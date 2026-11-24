#!/usr/bin/env python3
"""Builds the music bed of the README video from the 30 s MusicGen clip: copies of the clip joined with 3 s crossfades.

Usage, from this folder:
  python3 make_music.py --copies 4 --out voice/bed.wav [--bgm project/assets/audio/bgm0.wav]

N copies of a clip of L seconds last N x L - (N - 1) x 3 s. The clip is 29.94 s, so four copies last 110.76 s. mix.py
slows the bed by atempo 0.95, to 116.6 s, and needs it to last at least the film's duration plus 0.5 s afterwards.
Output: 32 kHz mono 16-bit WAV.
"""

import argparse
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
XFADE = 3.0


def duration(path):
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


def build(bgm, n, out):
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for _ in range(n):
        cmd += ["-i", bgm]
    if n == 1:
        cmd += ["-c:a", "pcm_s16le", out]
    else:
        fc, prev = [], "[0]"
        for i in range(1, n):
            last = i == n - 1
            fc.append(
                f"{prev}[{i}]acrossfade=d={XFADE:g}{'' if last else f'[a{i}]'}"
                + ("[o]" if last else "")
            )
            prev = f"[a{i}]"
        cmd += [
            "-filter_complex",
            ";".join(fc),
            "-map",
            "[o]",
            "-c:a",
            "pcm_s16le",
            out,
        ]
    subprocess.run(cmd, check=True)
    return duration(out)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--bgm", default=os.path.join(HERE, "project", "assets", "audio", "bgm0.wav")
    )
    ap.add_argument("--copies", type=int, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    got = build(a.bgm, a.copies, a.out)
    print(f"{a.copies} copies of {duration(a.bgm):.2f} s -> {a.out}: {got:.2f} s")


if __name__ == "__main__":
    main()
