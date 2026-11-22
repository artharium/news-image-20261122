#!/usr/bin/env python3
"""Entry program for news-image-20261122.

The image is drawn at build time by render.py (Pillow, on the build
machine) and committed as entry.png. This program only copies that
file to the grader's output directory, so it runs with the standard
library alone, needs no network, and writes identical bytes on
every run: a plain copy has no timestamp, no randomness and no
metadata of its own, so two runs produce the same sha256.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
