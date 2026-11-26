"""Admission and cache retention for the demo's single API worker."""

import asyncio
import re
import shutil
from dataclasses import replace

from starlette.responses import JSONResponse
from uvicorn._types import ASGIReceiveCallable, ASGISendCallable, Scope

from layerwise_bokeh.api._settings import load_settings
from layerwise_bokeh.api.main import create_app

_CACHE_SIZE = 6
_SEQUENCE_ID = re.compile(r"[0-9a-f]{16}")
_settings = load_settings()
_api = create_app(replace(_settings, cors_origins=()))
_generation = asyncio.Lock()
_video = asyncio.Lock()


def _prune_cache() -> None:
    if not _settings.sequences.is_dir():
        return
    entries = []
    for path in _settings.sequences.iterdir():
        if _SEQUENCE_ID.fullmatch(path.name) and path.is_dir():
            entries.append(path)
        elif path.name.startswith(".tmp-") and path.is_dir():
            shutil.rmtree(path)
    entries.sort(key=lambda path: path.stat().st_mtime_ns, reverse=True)
    for path in entries[_CACHE_SIZE:]:
        shutil.rmtree(path)


async def app(
    scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
) -> None:
    if scope["type"] != "http":
        await _api(scope, receive, send)
        return

    path = scope["path"].removeprefix(scope.get("root_path", ""))
    if scope["method"] == "POST" and path in ("/sequences", "/sequences/"):
        if _generation.locked():
            await JSONResponse(
                {"detail": "A sequence is generating. Try again when it finishes."},
                status_code=429,
            )(scope, receive, send)
            return

        # The API continues generation in its worker after a browser disconnects.
        # Keep consuming its progress so the admission slot is held until it finishes.
        body_complete = False
        disconnected = False

        async def receive_until_body_complete():
            nonlocal body_complete, disconnected
            message = await receive()
            if message["type"] == "http.request" and not message.get("more_body"):
                body_complete = True
            if message["type"] == "http.disconnect" and body_complete:
                disconnected = True
                await asyncio.Future()
            return message

        async def send_if_connected(message):
            nonlocal disconnected
            if not disconnected:
                try:
                    await send(message)
                except OSError:
                    disconnected = True

        async with _generation:
            await _api(scope, receive_until_body_complete, send_if_connected)
            async with _video:
                await asyncio.to_thread(_prune_cache)
        return

    if path.startswith("/sequences/"):
        # Encode at most one video at once and keep the file available until it is sent.
        async with _video:
            await _api(scope, receive, send)
        return

    await _api(scope, receive, send)
