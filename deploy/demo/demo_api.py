"""Admission and cache retention for the demo's single API worker."""

import asyncio
import re
import shutil
from contextlib import AsyncExitStack
from dataclasses import replace

from starlette.responses import JSONResponse
from starlette.types import Message, Receive, Scope, Send

from layerwise_bokeh.api._settings import load_settings
from layerwise_bokeh.api.main import NDJSON, create_app

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


async def _generate(scope: Scope, receive: Receive, send: Send) -> None:
    if _generation.locked():
        await JSONResponse(
            {"detail": "A sequence is generating. Try again when it finishes."},
            status_code=429,
        )(scope, receive, send)
        return

    body_complete = False
    disconnected = False
    messages = asyncio.Queue[Message | None]()
    response_end = None

    async def receive_until_body_complete() -> Message:
        nonlocal body_complete, disconnected
        message = await receive()
        if message["type"] == "http.request" and not message.get("more_body"):
            body_complete = True
        if message["type"] == "http.disconnect" and body_complete:
            disconnected = True
            await asyncio.Future()
        return message

    async def queue_response(message: Message) -> None:
        nonlocal response_end
        if message["type"] == "http.response.body" and not message.get("more_body"):
            response_end = message
            return
        if message["type"] == "http.response.start":
            headers = list(message.get("headers", ()))
            if (b"content-type", NDJSON.encode()) in headers:
                message = {
                    **message,
                    "headers": [*headers, (b"x-accel-buffering", b"no")],
                }
        messages.put_nowait(message)

    async def run_generation() -> None:
        try:
            try:
                await _api(scope, receive_until_body_complete, queue_response)
            finally:
                async with _video:
                    await asyncio.to_thread(_prune_cache)
        finally:
            _generation.release()
            # Finishing the response tells the client it can start another generation.
            if response_end is not None:
                messages.put_nowait(response_end)
            messages.put_nowait(None)

    # Progress is bounded by the frame limit. Drain it independently of network
    # writes so generation keeps its slot until the work and cache cleanup finish.
    await _generation.acquire()
    producer = asyncio.create_task(run_generation())
    try:
        while (message := await messages.get()) is not None:
            if not disconnected:
                try:
                    await send(message)
                except OSError:
                    disconnected = True
    finally:
        await asyncio.shield(producer)


async def _serve_video(scope: Scope, receive: Receive, send: Send) -> None:
    async with AsyncExitStack() as lookup:
        await lookup.enter_async_context(_video)
        start = None

        async def send_video(message: Message) -> None:
            nonlocal start
            if message["type"] == "http.response.start":
                start = message
                return
            if start is not None:
                # FileResponse opens the MP4 before its first body message, even
                # for Range requests. The open file survives cache eviction.
                await lookup.aclose()
                await send(start)
                start = None
            await send(message)

        # Require FileResponse to open the file itself if a server offers pathsend.
        if "http.response.pathsend" in scope.get("extensions", {}):
            scope = {
                **scope,
                "extensions": {
                    name: data
                    for name, data in scope["extensions"].items()
                    if name != "http.response.pathsend"
                },
            }
        await _api(scope, receive, send_video)


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    if scope["type"] == "http":
        path = scope["path"].removeprefix(scope.get("root_path", ""))
        if scope["method"] == "POST" and path in ("/sequences", "/sequences/"):
            await _generate(scope, receive, send)
            return
        if (
            scope["method"] == "GET"
            and path.startswith("/sequences/")
            and path.endswith(".mp4")
        ):
            await _serve_video(scope, receive, send)
            return
    await _api(scope, receive, send)
