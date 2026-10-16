# VD Veil Crosshair (experimental)

Visual-only, click-through crosshair overlay for **The Veil** from Roblox **Violence District**, targeting **KDE Plasma Wayland / CachyOS**. Vertical green dots, no horizontal lines. Separate profiles for ordinary spear and Through the Veil. No Roblox script injection or aim assist.

> **Uncalibrated test preset:** all current dot offsets are provisional. The supplied Oct 17 gameplay videos contain throws at various apparent distances but don't establish precise speed, drop, distances in studs, or a robust split between regular and special mode. These dots are NOT guaranteed aiming locations.

## Quick start: CachyOS / Arch Linux

```bash
sudo pacman -S --needed git python python-gobject python-cairo gtk3 gtk-layer-shell
git clone https://github.com/hiworld1231/vd-veil-crosshair.git
cd vd-veil-crosshair
python3 overlay.py
```

Launch Sober/Roblox on the **same monitor**. The overlay is transparent to mouse input, and doesn't aim or throw by itself. Fullscreen game is preferable for crosshair alignment. The overlay's layer-shell implementation supports Plasma Wayland but may need testing on your exact KWin and fullscreen setup.

In another terminal, while the overlay keeps running:

```bash
python3 switch.py normal       # ordinary spear
python3 switch.py special      # Through the Veil
python3 switch.py toggle       # toggle the profiles
python3 switch.py off          # hide
python3 switch.py on           # show again
```

You can bind `python3 /absolute/path/to/vd-veil-crosshair/switch.py toggle` to a KDE global shortcut. The overlay does not detect ability mode automatically.

## Calibration and settings

On first launch, the program creates:
`~/.config/vd-veil-crosshair/config.json`

Edit it while the overlay runs; changes reload automatically (about every 350ms). Relevant settings:

- `profiles.normal.dots_y`: ordinary spear dots **below** the central aim dot. Provisional preset: `[0, 19, 43, 76, 117, 166]`.
- `profiles.special.dots_y`: Through the Veil dots. Provisional preset: `[0, 12, 29, 51, 78, 109]`.
- `center_offset_x`, `center_offset_y`: adjust alignment. Positive Y moves downward. **Sober window title bar** seen in the footage is about 30px tall, which *may* require an approximately `15`px Y adjustment when the window reaches the bottom edge. Set `0` for a properly centered fullscreen viewport.
- `dot_radius`, `center_dot_radius`, `outline_width`, `opacity`, `color` adjust visuals.
- `reference_height` sets pixel scaling relative to 1080p. FOV changes invalidate calibration.

For a projectile with drop, **place a lower dot on the target**, meaning the actual camera aim is slightly above it. Shoot at nearby, medium and distant stationary targets while standing still, using the same charge level and FOV; record the overlay in-game. Change offsets based on actual impact locations. The mode-specific release delay may differ and is not measured here.

## Export transparent PNGs

If the native overlay isn't visible over fullscreen Roblox, or you're on X11, export reticle images for your preferred overlay tool:

```bash
python3 export_png.py --width 1920 --height 1080
```

Outputs:

- `out/veil_normal_1920x1080.png`
- `out/veil_special_1920x1080.png`

Both PNGs are fully transparent except for the dots, and are intended to be displayed at their native resolution.

## Troubleshooting

- `echo $XDG_SESSION_TYPE` should print `wayland`; otherwise use exported PNGs.
- Arch system Python is required for installed PyGObject. Avoid an isolated venv unless it has GI bindings.
- If dots aren't visible, first test outside exclusive fullscreen, verify opacity, and check monitor and viewport alignment.
- Stop the overlay with Ctrl+C in the terminal. `switch.py off` merely hides it.
- Dot marks are not distance measurements in studs; don't infer a real trajectory from the provisional presets.

**Planned next step:** inspect another recording with the overlay visible on targets of varying distances; refine profiles separately.


## Quick calibration without editing JSON

```bash
python3 tune.py normal --stretch 1.15    # spread normal dots
python3 tune.py special --stretch 0.9    # compress special dots
python3 tune.py normal --dots "0,19,43,76,117,166"
python3 tune.py --center-y 15           # compensate Sober title bar if needed
python3 tune.py normal                 # show current offsets
```
