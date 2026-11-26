#!/usr/bin/env python3
"""Assemble the demo container build context from the current checkout."""

import argparse
import filecmp
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPLOY = ROOT / "deploy/demo"
LIBRARY = Path("backend/data/library_demo")
ESTIMATORS = ("da2-base", "da2-large", "da2-small", "depth-pro")
DEMO_FILES = (
    ".dockerignore",
    "Dockerfile",
    "nginx.conf",
    "demo_api.py",
    "start.sh",
)
SOURCE_PATHS = (
    "pyproject.toml",
    "uv.lock",
    "backend/pyproject.toml",
    "backend/src",
    "frontend/next.config.ts",
    "frontend/package.json",
    "frontend/pnpm-lock.yaml",
    "frontend/pnpm-workspace.yaml",
    "frontend/postcss.config.mjs",
    "frontend/src",
    "frontend/tsconfig.json",
)


def _copy(source: Path, target: Path) -> None:
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"Expected a regular file at {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def _copy_library(stage: Path) -> None:
    for estimator in ESTIMATORS:
        for kind, count, files in (
            (
                "foregrounds",
                7,
                (
                    "alpha.png",
                    "depth.png",
                    "depth_input.png",
                    "depth_raw.png",
                    "meta.json",
                    "rgb.png",
                ),
            ),
            ("backgrounds", 1, ("depth.png", "rgb.png")),
        ):
            relative = LIBRARY / estimator / kind
            assets = sorted(
                path
                for path in (ROOT / relative).iterdir()
                if not path.name.startswith(".")
            )
            if len(assets) != count or any(
                path.is_symlink() or not path.is_dir() for path in assets
            ):
                raise ValueError(f"Expected {count} asset directories in {relative}")
            for asset in assets:
                for file in files:
                    _copy(asset / file, stage / relative / asset.name / file)


def _identical(out: Path, stage: Path) -> bool:
    expected = sorted(path.relative_to(stage) for path in stage.rglob("*"))
    actual = sorted(path.relative_to(out) for path in out.rglob("*"))
    return expected == actual and all(
        not (out / path).is_symlink()
        and (
            (out / path).is_dir()
            if (stage / path).is_dir()
            else filecmp.cmp(out / path, stage / path, shallow=False)
        )
        for path in expected
    )


def assemble(out: Path) -> None:
    if out.is_symlink():
        raise ValueError(f"Output must not be a symlink: {out}")
    out = out.resolve()
    if out.is_relative_to(ROOT) or ROOT.is_relative_to(out):
        raise ValueError("Choose an output directory outside the repository.")
    out.parent.mkdir(parents=True, exist_ok=True)
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z", "--", *SOURCE_PATHS], cwd=ROOT
    )
    with tempfile.TemporaryDirectory(prefix=".demo-", dir=out.parent) as tmp:
        stage = Path(tmp) / "demo"
        for path in tracked.decode().split("\0"):
            if path:
                _copy(ROOT / path, stage / path)
        for file in DEMO_FILES:
            _copy(DEPLOY / file, stage / file)
        _copy_library(stage)
        if out.exists():
            if not out.is_dir():
                raise ValueError(f"Output must be a directory: {out}")
            if any(out.iterdir()):
                if _identical(out, stage):
                    return
                raise ValueError(
                    f"Output has other content: {out}. Choose an empty directory."
                )
        stage.rename(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        assemble(args.out)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")
    print(args.out.resolve())
