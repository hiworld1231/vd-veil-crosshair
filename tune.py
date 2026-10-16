#!/usr/bin/env python3
"""Calibrate vertical aiming marks. All offsets are in 1080p reference pixels."""
import argparse
import json

from reticle import config_path, load_config

parser = argparse.ArgumentParser(description="Tune VD Veil aiming marks without editing JSON")
parser.add_argument("profile", nargs="?", choices=("normal", "special"), default="normal")
parser.add_argument("--zero-y", type=float, help="zero aim position: -40 moves zero dot 40px ABOVE screen centre")
parser.add_argument("--center-y", type=float, help="viewport alignment only; normally leave at 0")
parser.add_argument("--stretch", type=float, help="multiply existing vertical marks' distances")
parser.add_argument("--dots", help='replace vertical offsets, e.g. "0,20,45,90"')
parser.add_argument("--dot", nargs=2, type=float, metavar=("INDEX", "Y"), help="set a single dot: index 1 is first below the zero, Y is px below zero")
args = parser.parse_args()
cfg = load_config()
profile = cfg["profiles"][args.profile]

requested = sum(v is not None for v in (args.stretch, args.dots, args.dot))
if requested > 1:
    parser.error("Use only one of --stretch, --dots or --dot")
if args.stretch is not None and not 0.2 <= args.stretch <= 5:
    parser.error("--stretch must be between 0.2 and 5")

if args.dots is not None:
    try:
        values = [float(s.strip()) for s in args.dots.split(",")]
    except ValueError:
        parser.error("--dots must be a comma-separated list of numbers")
elif args.stretch is not None:
    values = [round(float(d) * args.stretch, 1) for d in profile["dots_y"]]
elif args.dot is not None:
    raw_index, value = args.dot
    index = int(raw_index)
    if raw_index != index or index < 1 or index >= len(profile["dots_y"]):
        parser.error(f"INDEX must be 1..{len(profile['dots_y'])-1}")
    values = [float(d) for d in profile["dots_y"]]
    values[index] = value
else:
    values = None

if values is not None:
    if not (1 <= len(values) <= 20 and values[0] == 0 and
            all(0 <= a < b <= 1000 for a, b in zip(values, values[1:]))):
        parser.error("dots must start at 0 and strictly increase; max 20 dots and max 1000px")
    profile["dots_y"] = values

if args.zero_y is not None:
    profile["zero_y"] = args.zero_y
if args.center_y is not None:
    cfg["center_offset_y"] = args.center_y
if any(v is not None for v in (args.dots, args.stretch, args.dot, args.zero_y, args.center_y)):
    target = config_path()
    tmp = target.with_suffix(".tmp")
    tmp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(target)

print(f"{args.profile}: zero_y={profile.get('zero_y', 40)} px")
print(f"  dots_y={profile['dots_y']}")
print(f"  center_offset_y={cfg.get('center_offset_y', 0)} px (viewport only)")
