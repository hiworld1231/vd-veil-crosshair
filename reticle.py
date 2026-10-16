"""Shared reticle geometry for PNG export and the Wayland overlay."""
from __future__ import annotations

import json
import os
from pathlib import Path

APP_NAME = "vd-veil-crosshair"
DEFAULT_CONFIG = Path(__file__).with_name("config.example.json")


def config_path() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / APP_NAME / "config.json"


def load_config() -> dict:
    path = config_path()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(DEFAULT_CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    return json.loads(path.read_text(encoding="utf-8"))


def set_profile(selection: str) -> str:
    config = load_config()
    if selection == "toggle":
        selection = "special" if config.get("active_profile") == "normal" else "normal"
    if selection == "off":
        config["enabled"] = False
    elif selection in ("normal", "special"):
        config["enabled"] = True
        config["active_profile"] = selection
    elif selection == "on":
        config["enabled"] = True
    else:
        raise ValueError(f"Unknown selection: {selection}")
    target = config_path()
    temp = target.with_suffix(".tmp")
    temp.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(target)
    return f"{'on' if config['enabled'] else 'off'}, profile={config['active_profile']}"


def _rgb(hex_color: str) -> tuple[float, float, float]:
    value = hex_color.lstrip("#")
    if len(value) != 6:
        raise ValueError("Color must be #RRGGBB")
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))


def paint(ctx, config: dict, width: int, height: int) -> None:
    """Draw in pixel units normalized to reference_height (1080 by default).

    Positive Y is down; put a lower dot on a target to compensate for drop.
    """
    if not config.get("enabled", True):
        return
    profile_name = config.get("active_profile", "normal")
    profile = config["profiles"][profile_name]
    factor = height / max(1, float(config.get("reference_height", 1080)))
    x = width / 2 + float(config.get("center_offset_x", 0)) * factor
    # Profile zeroing is a real aiming correction, distinct from viewport alignment.
    # Legacy configs without zero_y inherit the user's known working -40px baseline.
    zero_y = float(profile.get("zero_y", -40))
    y = height / 2 + (float(config.get("center_offset_y", 0)) + zero_y) * factor
    size = max(0.5, float(config.get("dot_radius", 1.5)) * factor)
    stroke = max(0.5, float(config.get("outline_width", 1.0)) * factor)
    alpha = max(0, min(1, float(config.get("opacity", 0.94))))
    fg = _rgb(config.get("color", "#83FFC1"))
    outline = _rgb(config.get("outline_color", "#081610"))
    ctx.save()
    for offset in profile["dots_y"]:
        y_dot = y + float(offset) * factor
        r = max(0.5, float(config.get("center_dot_radius", 1.6)) * factor) if offset == 0 else size
        ctx.new_path()
        ctx.arc(x, y_dot, r + stroke, 0, 6.283185307179586)
        ctx.set_source_rgba(*outline, alpha)
        ctx.fill()
        ctx.new_path()
        ctx.arc(x, y_dot, r, 0, 6.283185307179586)
        ctx.set_source_rgba(*fg, alpha)
        ctx.fill()
    ctx.restore()
