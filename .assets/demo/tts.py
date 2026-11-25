"""Synthesizes the voice clips of voice/lines.tsv with Kokoro (af_heart) through the HyperFrames CLI.

Usage, from this folder:
  HYPERFRAMES_PYTHON=<venv>/bin/python python3 tts.py [--speed 0.97] [V1 V2 ...]

Writes voice/vo/<id>_<speed>.wav for every line, or for the ids named. Checks the SHA-256 of
the two model files before and after, so a fresh download is checked too, and stops on a
mismatch. Needs the network only on the first run, when HyperFrames downloads the model into
~/.cache/hyperframes/tts/. The fit rule lives in mix.py: it takes, per line, the first of the
speeds 0.97, 1.03 and 1.08 whose clip ends before its latest end, so synthesize the slower
speeds only for the lines that overrun.
"""

import argparse
import hashlib
import os
import subprocess
import sys

import mix

HF_TTS_VERSION = "0.9.81"
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.expanduser("~/.cache/hyperframes/tts/models/kokoro-v1.0.onnx")
VOICES = os.path.expanduser("~/.cache/hyperframes/tts/voices/voices-v1.0.bin")
SHA = {
    MODEL: "7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5",
    VOICES: "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d",
}


def check_models(when):
    """Stop when a model file exists and its SHA-256 differs; stop too if one is missing after a run."""
    for path, sha in SHA.items():
        if not os.path.exists(path):
            if when == "after":
                sys.exit(f"model file missing after synthesis: {path}")
            continue
        with open(path, "rb") as f:
            got = hashlib.sha256(f.read()).hexdigest()
        if got != sha:
            sys.exit(
                f"model file {when} synthesis has a different SHA-256 ({got[:12]}, expected {sha[:12]}): {path}"
            )


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--lines", default=os.path.join(HERE, "voice", "lines.tsv"))
    ap.add_argument(
        "--out", default=os.path.join(HERE, "voice", "vo"), help="folder for the clips"
    )
    ap.add_argument("--speed", default="0.97")
    ap.add_argument("ids", nargs="*")
    a = ap.parse_args()
    if "HYPERFRAMES_PYTHON" not in os.environ:
        sys.exit("set HYPERFRAMES_PYTHON to the Kokoro venv's python")
    check_models("before")
    lines = mix.read_lines(a.lines)
    os.makedirs(a.out, exist_ok=True)
    for i in a.ids or list(lines):
        dst = os.path.join(a.out, f"{i}_{a.speed}.wav")
        r = subprocess.run(
            [
                "npx",
                "--yes",
                f"hyperframes@{HF_TTS_VERSION}",
                "tts",
                lines[i][2],
                "-v",
                "af_heart",
                "-s",
                a.speed,
                "-o",
                dst,
            ],
            capture_output=True,
            text=True,
        )
        print(i, r.returncode, dst if r.returncode == 0 else r.stderr[-300:])
        if r.returncode != 0:
            sys.exit(1)
        check_models("after")


if __name__ == "__main__":
    main()
