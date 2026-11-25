"""Mixes the voice and the music bed of the README video into voice/work/mix.wav and voice/work/mix-report.txt.

Usage, from this folder:
  python3 mix.py [voice/mix.json] [--work DIR] [--voice DIR]

voice/mix.json holds the settings; its paths are relative to its own folder:
  duration  seconds of the film
  lines     lines.tsv: id, start, latest end, text (tab separated, # comments)
  voice     folder with the clips <id>_<speed>.wav that tts.py writes
  music     {"bed": wav, "atempo": 0.95, "fade_in": 1.2, "fade_out": [start, end]}; make_music.py builds the bed
  mix       optional, overrides DEFAULTS below

Steps: the clips go to their start on a mono bus, none overlapping -> gain to voice_lufs, alimiter -> the bed is
slowed by atempo and brought to bed_lufs -> a side-chain compressor keyed by the voice ducks it -> linear fades,
silent from the end of fade_out -> sum -> final alimiter -> trim to the duration. With "target_lufs" set, the sum is
raised or lowered until the file measures that loudness. With "duck_threshold" null, it is tuned until the voice
stands "target_gap" dB over the ducked bed on average. Loudness is BS.1770-4 gated (ffmpeg ebur128).
Per line, the first of the speeds 0.97, 1.03 and 1.08 whose clip ends before its latest end is used; a line that
fits at none stops the run, and the fix is a longer window, never new wording.
Needs numpy and ffmpeg.
"""

import argparse
import json
import os
import re
import subprocess
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = {
    "sr": 48000,
    "voice_lufs": -18.0,
    "bed_lufs": -25.0,
    "voice_limit": 0.82,
    "final_limit": 0.75,
    "limiter_latency": 1,
    "target_lufs": -18.0,
    "duck_threshold": None,
    "duck_ratio": 4,
    "target_gap": 10.5,
    "speeds": ["0.97", "1.03", "1.08"],
    "measure": None,
    "pad": None,
    "min_gap": 0.3,
}


def write_wav(path, sr, arr):
    a = np.clip(arr, -1, 1)
    a = (a * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1 if a.ndim == 1 else a.shape[1])
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(a.tobytes())


def read_wav(path):
    with wave.open(path) as w:
        n, ch = w.getnframes(), w.getnchannels()
        a = np.frombuffer(w.readframes(n), "<i2").reshape(-1, ch)
        return w.getframerate(), (a[:, 0] if ch == 1 else a)


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def lufs(path):
    """Integrated loudness, true peak and loudness range of a file through ebur128."""
    r = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            path,
            "-af",
            "ebur128=peak=true",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    t = r.stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", t)[-1]
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", t)[-1]
    lra = re.findall(r"LRA:\s+([\d.]+) LU", t)[-1]
    return float(i), float(tp), float(lra)


def read_lines(path):
    """lines.tsv -> {id: (start, latest_end, text)} in file order."""
    rows = {}
    with open(path, encoding="utf-8") as f:
        for ln in f:
            if not ln.strip() or ln.startswith("#"):
                continue
            i, start, end, text = ln.rstrip("\n").split("\t")
            rows[i] = (float(start), float(end), text)
    return rows


def load_clip(p, sr):
    r = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            p,
            "-f",
            "f32le",
            "-ac",
            "1",
            "-ar",
            str(sr),
            "-",
        ],
        capture_output=True,
        check=True,
    )
    return np.frombuffer(r.stdout, np.float32).copy()


def trim_clip(x, thr=0.003):
    idx = np.where(np.abs(x) > thr)[0]
    return x[idx[0] : idx[-1] + 1]


def fit_clip(i, start, latest, vo, speeds, sr):
    """The first speed whose clip ends before its latest end. Returns (samples, speed)."""
    for sp in speeds:
        p = os.path.join(vo, f"{i}_{sp}.wav")
        if not os.path.exists(p):
            continue
        x = trim_clip(load_clip(p, sr))
        if start + len(x) / sr <= latest:
            return x, sp
    raise SystemExit(
        f"{i}: overruns its latest end at every speed {speeds}: lengthen the window under it"
    )


def build(film_path, work, voice_dir=None):
    with open(film_path, encoding="utf-8") as f:
        film = json.load(f)
    base = os.path.dirname(os.path.abspath(film_path))

    def rel(p):
        return p if os.path.isabs(p) else os.path.join(base, p)

    cfg = dict(DEFAULTS)
    cfg.update(film.get("mix", {}))
    music = film["music"]
    SR, DUR = int(cfg["sr"]), float(film["duration"])
    N = int(round(DUR * SR))
    MEASURE = cfg["measure"] if cfg["measure"] is not None else DUR + 1.0
    PAD = cfg["pad"] if cfg["pad"] is not None else int(np.ceil(DUR + 4.5))
    lines = read_lines(rel(film["lines"]))
    vo = voice_dir or rel(film.get("voice", "vo"))
    os.makedirs(work, exist_ok=True)

    def W(name):
        return os.path.join(work, name)

    latency = ":latency=1" if cfg["limiter_latency"] else ""
    rep = []

    def P(*x):
        rep.append(" ".join(str(i) for i in x))

    # ---- voice bus ----
    bus = np.zeros(N, np.float32)
    prev_end, spans = 0, []
    for i, (start, latest, _) in lines.items():
        x, sp = fit_clip(i, start, latest, vo, cfg["speeds"], SR)
        a = int(round(start * SR))
        b = a + len(x)
        assert a >= prev_end, f"{i} overlaps the previous line"
        if spans and start - spans[-1][3] < cfg["min_gap"] - 1e-6:
            P(
                f"WARNING {i} starts {start - spans[-1][3]:.2f} s after the previous line (rule: {cfg['min_gap']} s)"
            )
        bus[a:b] += x
        prev_end = b
        spans.append((i, sp, start, b / SR, latest))
        P(
            f"{i:<4} speed {sp} start {start:6.2f} end {b / SR:6.2f} "
            f"latest {latest:6.2f} slack {latest - b / SR:5.2f}"
        )
    write_wav(W("voice_raw.wav"), SR, bus)
    raw = W("voice_raw.wav")
    li = lufs(raw)[0]
    vlim = f"alimiter=limit={cfg['voice_limit']}:attack=3:release=40:level=0{latency}"
    gdb = cfg["voice_lufs"] - li
    for _ in range(6):
        sh(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-i",
                raw,
                "-af",
                f"volume={gdb}dB,aformat=channel_layouts=stereo,{vlim}",
                W("voice.wav"),
            ]
        )
        vi, vtp, _ = lufs(W("voice.wav"))
        if abs(vi - cfg["voice_lufs"]) < 0.05:
            break
        gdb += cfg["voice_lufs"] - vi
    P(
        f"voice raw {li} LUFS, gain {gdb:.2f} dB; voice bus {vi} LUFS, true peak {vtp} dBTP"
    )
    v = read_wav(W("voice.wav"))[1][:, 0].astype(np.float32) / 32768

    # ---- bed: slowed, gain for bed_lufs over the first `measure` seconds ----
    bed = W("bed.wav")
    sh(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-i",
            rel(music["bed"]),
            "-af",
            f"atempo={music['atempo']},aresample={SR},aformat=channel_layouts=stereo",
            bed,
        ]
    )
    bed_len = float(
        sh(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "csv=p=0",
                bed,
            ]
        ).stdout.strip()
    )
    assert bed_len >= DUR + 0.5, (
        f"the bed is {bed_len:.1f} s long, the film {DUR} s: build a longer bed with make_music.py"
    )
    sh(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-i",
            bed,
            "-af",
            f"atrim=0:{MEASURE}",
            W("bed_measure.wav"),
        ]
    )
    bl = lufs(W("bed_measure.wav"))[0]
    g = 10 ** ((cfg["bed_lufs"] - bl) / 20)
    P(f"bed {bl} LUFS, gain {20 * np.log10(g):.2f} dB, length {bed_len:.2f} s")
    sh(
        [
            "ffmpeg",
            "-v",
            "error",
            "-y",
            "-i",
            W("voice.wav"),
            "-af",
            f"apad=whole_dur={PAD}",
            W("voice_pad.wav"),
        ]
    )

    def duck(thr):
        out = W("music_ducked_raw.wav")
        sh(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-i",
                W("voice_pad.wav"),
                "-i",
                bed,
                "-filter_complex",
                f"[1:a]volume={g},apad=whole_dur={PAD}[m];[m][0:a]sidechaincompress=threshold={thr}:ratio={cfg['duck_ratio']}:attack=20:release=600:makeup=1[o]",
                "-map",
                "[o]",
                out,
            ]
        )
        d = read_wav(out)[1].astype(np.float32) / 32768
        assert len(d) >= N, len(d)
        return d[:N]

    def gaps(dm):
        return [
            20
            * np.log10(
                np.sqrt(np.mean(v[int(s * SR) : int(e * SR)] ** 2))
                / np.sqrt(np.mean(dm[int(s * SR) : int(e * SR), 0] ** 2))
            )
            for _, _, s, e, _ in spans
        ]

    thr = cfg["duck_threshold"]
    if thr is None:
        lo, hi = 0.02, 0.6
        for _ in range(8):
            thr = float(np.sqrt(lo * hi))
            if float(np.mean(gaps(duck(thr)))) > cfg["target_gap"]:
                lo = thr
            else:
                hi = thr
        thr = round(float(np.sqrt(lo * hi)), 3)
    dm = duck(thr)
    P(f"ducking threshold {thr}, ratio {cfg['duck_ratio']}")

    # ---- fades, then the sum and the final limiter ----
    t = np.arange(N) / SR
    f_out = music["fade_out"]
    env = np.clip(t / music["fade_in"], 0, 1) * np.clip(
        (f_out[1] - t) / round(f_out[1] - f_out[0], 6), 0, 1
    )
    dm = dm * env[:, None]
    write_wav(W("music_ducked.wav"), SR, dm)
    vv = np.stack([v, v], 1)
    flim = f"alimiter=limit={cfg['final_limit']}:attack=5:release=50:level=0{latency}"
    mix = W("mix.wav")

    def final(gain_db=0.0):
        s = vv + dm if gain_db == 0.0 else (vv + dm) * 10 ** (gain_db / 20)
        write_wav(W("sum.wav"), SR, s)
        sh(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-i",
                W("sum.wav"),
                "-af",
                f"{flim},atrim=0:{DUR:g},asetpts=N/SR/TB",
                "-ar",
                str(SR),
                "-c:a",
                "pcm_s16le",
                mix,
            ]
        )
        return lufs(mix)

    m = final()
    trim_db = 0.0
    if cfg["target_lufs"] is not None:
        for _ in range(4):
            if abs(m[0] - cfg["target_lufs"]) < 0.03:
                break
            trim_db += cfg["target_lufs"] - m[0]
            m = final(trim_db)
        if abs(trim_db) > 1e-9:
            P(
                f"final trim {trim_db:+.2f} dB to reach {cfg['target_lufs']} LUFS (voice and bed together)"
            )

    # ---- report ----
    P(f"mix: {m[0]} LUFS, LRA {m[2]}, true peak {m[1]} dBTP")
    mx = read_wav(mix)[1].astype(np.float32) / 32768
    tail = np.abs(mx[-int(0.1 * SR) :]).max() if len(mx) else 0
    P(f"last 0.1 s peak {20 * np.log10(tail + 1e-9):.1f} dBFS")
    gp = gaps(dm)
    P(
        "voice minus ducked music (dB, rms in speech windows): "
        + " ".join(f"{x:.1f}" for x in gp)
        + f" mean {np.mean(gp):.1f}"
    )
    with open(W("mix-report.txt"), "w") as f:
        f.write("\n".join(rep) + "\n")
    print("\n".join(rep))
    return mix


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("film", nargs="?", default=os.path.join(HERE, "voice", "mix.json"))
    ap.add_argument(
        "--work", default=os.path.join(HERE, "voice", "work"), help="output folder"
    )
    ap.add_argument(
        "--voice",
        default=None,
        help="folder with the clips (default the mix file's voice)",
    )
    a = ap.parse_args()
    build(a.film, a.work, a.voice)


if __name__ == "__main__":
    main()
