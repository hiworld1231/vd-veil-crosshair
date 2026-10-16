#!/usr/bin/env python3
"""Tune both profiles without editing JSON by hand."""
import argparse
import json

from reticle import config_path, load_config

parser = argparse.ArgumentParser(description="Quickly calibrate VD Veil reticle spacing")
parser.add_argument("profile", nargs="?", choices=("normal", "special"), default="normal")
parser.add_argument("--stretch", type=float, help="multiply dot distances, e.g. 1.15 farther / 0.85 closer")
parser.add_argument("--dots", help='replace dot offsets, e.g. "0,18,45,80,120"')
parser.add_argument("--center-y", type=float, help="viewport center shift (15 for windowed Sober)")
args = parser.parse_args()
cfg = load_config()
if args.stretch is not None and not 0.2 <= args.stretch <= 5:
    parser.error("--stretch must be between 0.2 and 5")
if args.dots is not None and args.stretch is not None:
    parser.error("Choose --dots OR --stretch")

if args.dots is not None:
    try:
        values = [float(s.strip()) for s in args.dots.split(",")]
    except ValueError:
        parser.error("--dots must contain comma-separated numbers")
    if not (2 <= len(values) <= 20 and values[0] == 0 and all(a < b for a, b in zip(values, values[1:]))):
        parser.error("dots must start at zero and be strictly increasing (2-20 dots)")
    cfg["profiles"][args.profile]["dots_y"] = values
elif args.stretch is not None:
    cfg["profiles"][args.profile]["dots_y"] = [round(float(d) * args.stretch, 1) for d in cfg["profiles"][args.profile]["dots_y"]]
if args.center_y is not None:
    cfg["center_offset_y"] = args.center_y

if args.dots is not None or args.stretch is not None or args.center_y is not None:
    path = config_path()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)

print(f'{args.profile}: {cfg["profiles"][args.profile]["dots_y"]}')
print(f'center_offset_y: {cfg["center_offset_y"]}')
