#!/usr/bin/env python3
"""Save transparent full-resolution images for PNG-capable overlay programs."""
import argparse
from pathlib import Path

try:
    import cairo
except ImportError:
    raise SystemExit("Install python-cairo: sudo pacman -S python-cairo")

from reticle import load_config, paint

parser = argparse.ArgumentParser(description="Export reticles to transparent PNGs")
parser.add_argument("--width", type=int, default=1920)
parser.add_argument("--height", type=int, default=1080)
parser.add_argument("--out", type=Path, default=Path("out"))
args = parser.parse_args()
if not (100 <= args.width <= 8192 and 100 <= args.height <= 8192):
    raise SystemExit("Invalid output size")
args.out.mkdir(parents=True, exist_ok=True)
original = load_config()
for name in ("normal", "special"):
    cfg = {**original, "enabled": True, "active_profile": name}
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, args.width, args.height)
    ctx = cairo.Context(surface)
    paint(ctx, cfg, args.width, args.height)
    result = args.out / f"veil_{name}_{args.width}x{args.height}.png"
    surface.write_to_png(str(result))
    print(result)
