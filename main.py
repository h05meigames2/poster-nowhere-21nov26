"""VELMORA — The Poster for a Place That Isn't There.

A travel poster for an invented place: VELMORA, a floating city above
the clouds, drawn entirely in code by this program (standard library
only — no images, no fonts, no network, no third-party packages).

Run:  python3 main.py
Writes: /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png; falls back
        to ./out/entry.png when /output is not writable, e.g. locally)
Size:   1024x1024 PNG, deterministic — every run writes identical bytes.
"""

import hashlib
import os
import sys

from canvas import Canvas
from scene import W, H, draw_poster


def resolve_output_dir():
    preferred = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(preferred, exist_ok=True)
        probe = os.path.join(preferred, ".write-test")
        with open(probe, "w") as f:
            f.write("ok")
        os.remove(probe)
        return preferred
    except OSError:
        fallback = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "out")
        os.makedirs(fallback, exist_ok=True)
        return fallback


def main():
    out_dir = resolve_output_dir()
    out_path = os.path.join(out_dir, "entry.png")
    canvas = Canvas(W, H)
    draw_poster(canvas)
    png = canvas.to_png()
    with open(out_path, "wb") as f:
        f.write(png)
    digest = hashlib.sha256(png).hexdigest()
    print(f"wrote {out_path} ({len(png)} bytes, {W}x{H})")
    print(f"sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
