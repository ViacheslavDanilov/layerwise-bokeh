"""Exercise the demo's single-worker admission and file delivery as ASGI requests."""

import asyncio
import importlib.util
import os
from pathlib import Path

import pytest
from starlette.responses import JSONResponse, StreamingResponse

_DEMO = Path(__file__).resolve().parents[3] / "deploy/demo/demo_api.py"


@pytest.fixture
def demo(tmp_path, monkeypatch):
    monkeypatch.setenv("LAYERWISE_BOKEH_DATA_ROOT", str(tmp_path))
    spec = importlib.util.spec_from_file_location("demo_api", _DEMO)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def _request(app, method, path, *, headers=(), stall=None):
    scope = {
        "type": "http",
        "asgi": {"spec_version": "2.3"},
        "method": method,
        "path": f"/api{path}",
        "root_path": "/api",
        "query_string": b"",
        "headers": list(headers),
    }
    request_sent = False
    messages = []

    async def receive():
        nonlocal request_sent
        if not request_sent:
            request_sent = True
            return {"type": "http.request", "body": b"{}", "more_body": False}
        await asyncio.Future()

    async def send(message):
        if stall is not None and message["type"] == "http.response.body":
            stalled, resume = stall
            stalled.set()
            await resume.wait()
        messages.append(message)

    await app(scope, receive, send)
    return messages


def test_stalled_video_allows_another_video_and_generation(demo, tmp_path, monkeypatch):
    root = tmp_path / "sequences"
    # The first video spans multiple FileResponse chunks so it must read again
    # after pruning removes its directory.
    clip = b"video bytes" * 12_000
    for index in range(7):
        sequence = root / f"{index:016x}"
        sequence.mkdir(parents=True)
        (sequence / "sequence.json").touch()
        (sequence / "bokeh.mp4").write_bytes(clip)
        os.utime(sequence, (index + 1, index + 1))

    async def check():
        stalled, resume = asyncio.Event(), asyncio.Event()
        generating, finish = asyncio.Event(), asyncio.Event()
        api = demo._api

        async def upstream(scope, receive, send):
            if scope["method"] == "POST":
                await receive()
                generating.set()
                await finish.wait()
                await StreamingResponse(
                    iter([b"{}\n"]), media_type="application/x-ndjson"
                )(scope, receive, send)
            else:
                await api(scope, receive, send)

        monkeypatch.setattr(demo, "_api", upstream)
        slow = asyncio.create_task(
            _request(
                demo.app,
                "GET",
                "/sequences/0000000000000000/bokeh.mp4",
                stall=(stalled, resume),
            )
        )
        generation = asyncio.create_task(_request(demo.app, "POST", "/sequences"))
        try:
            async with asyncio.timeout(5):
                await stalled.wait()
                await generating.wait()
                rejected = await _request(demo.app, "POST", "/sequences")
            assert rejected[0]["status"] == 429

            finish.set()
            video = asyncio.create_task(
                _request(
                    demo.app,
                    "GET",
                    "/sequences/0000000000000001/bokeh.mp4",
                    headers=[(b"range", b"bytes=6-10")],
                )
            )
            done, _ = await asyncio.wait({video, generation}, timeout=2)
            assert done == {video, generation}, (
                f"While the first video was stalled, the second video finished: "
                f"{video.done()}, generation finished: {generation.done()}"
            )
            assert video.result()[0]["status"] == 206
            assert video.result()[1]["body"] == b"bytes"
            headers = dict(generation.result()[0]["headers"])
            assert headers[b"x-accel-buffering"] == b"no"
            assert len(list(root.iterdir())) == 6
            assert not (root / "0000000000000000").exists()
            assert not slow.done()

            next_generation = await asyncio.wait_for(
                _request(demo.app, "POST", "/sequences"), timeout=2
            )
            assert next_generation[0]["status"] == 200
        finally:
            finish.set()
            resume.set()
        complete_video = await slow
        assert b"".join(message["body"] for message in complete_video[1:]) == clip

    asyncio.run(check())


@pytest.mark.parametrize("disconnect", [False, True], ids=["stalled", "disconnected"])
def test_generation_releases_admission_after_failed_work(
    demo, tmp_path, monkeypatch, disconnect
):
    partial = tmp_path / "sequences" / ".tmp-failed"

    async def check():
        sent_progress, resume, finish = (
            asyncio.Event(),
            asyncio.Event(),
            asyncio.Event(),
        )

        async def upstream(scope, receive, send):
            await receive()
            if scope["path"].endswith("/"):
                assert not partial.exists()
                await JSONResponse({"ok": True})(scope, receive, send)
                return

            async def progress():
                partial.mkdir(parents=True)
                yield b'{"done": 1}\n'
                await finish.wait()
                raise RuntimeError("generation failed")

            await StreamingResponse(progress(), media_type="application/x-ndjson")(
                scope, receive, send
            )

        async def client(scope, receive, send):
            async def send_progress(message):
                if message["type"] == "http.response.body":
                    sent_progress.set()
                    if disconnect:
                        raise BrokenPipeError
                    await resume.wait()
                await send(message)

            await demo.app(scope, receive, send_progress)

        monkeypatch.setattr(demo, "_api", upstream)
        first = asyncio.create_task(_request(client, "POST", "/sequences"))
        try:
            async with asyncio.timeout(5):
                await sent_progress.wait()
                rejected = await _request(demo.app, "POST", "/sequences")
                assert rejected[0]["status"] == 429

                finish.set()
                # A second generation can start while the first response is
                # still stalled or its client has disconnected.
                while True:
                    response = await _request(demo.app, "POST", "/sequences/")
                    if response[0]["status"] != 429:
                        break
                    await asyncio.sleep(0.01)
                assert response[0]["status"] == 200
                assert b"x-accel-buffering" not in dict(response[0]["headers"])
        finally:
            finish.set()
            resume.set()
            with pytest.raises(RuntimeError, match="generation failed"):
                await first

    asyncio.run(check())
