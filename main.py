# main.py — entrypoint for news-image-20261123.
# Renders one 1024x1024 PNG that sums up Monday 23 November 2026's world
# news and writes it to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png).
# Deterministic: no network, no clock, no randomness — two runs produce
# byte-identical output.
#
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import render

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    img = render()
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
