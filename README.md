# VD Veil Crosshair (experimental)

Visual-only, click-through crosshair overlay for **The Veil** from Roblox **Violence District**, targeting **KDE Plasma Wayland / CachyOS**. Vertical green dots, no horizontal lines. Separate profiles for ordinary spear and Through the Veil. No Roblox script injection or aim assist.

> **Uncalibrated test preset:** only the approximate **-40px zero point for normal throws** comes from player testing. All other vertical marks are illustrative and must be calibrated in-game. The special-ability zero point is also provisional. This overlay does not read distance from Roblox.

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

- `profiles.normal.zero_y`: zero/reference point offset. Default `-40` in reference pixels based on the user's already useful existing crosshair (NOT a computed ballistic correction).
- `profiles.special.zero_y`: independent zero point for Through the Veil. Starts at `-40` only until measured.
- `profiles.normal.dots_y`: marks BELOW the zero point, to place on targets at progressively greater ranges. Values are test placeholders: `[0, 19, 43, 76, 117, 166]`.
- `profiles.special.dots_y`: Through the Veil dots. Provisional preset: `[0, 12, 29, 51, 78, 109]`.
- `center_offset_x`, `center_offset_y`: viewport alignment ONLY. Normally leave at `0` in fullscreen; these are not ballistic offsets. For aim correction use profile `zero_y` instead. Positive values move down. Configs from the first release without `zero_y` still use -40 via fallback.
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


## Calibrate ONLY throw height (without measuring studs)

First update the project and launch the new mouse-transparent overlay:

```bash
git pull
python3 overlay.py
```

In a different terminal while it is running, use these commands:

```bash
python3 tune.py normal --zero-y -40    # known starting zero for the NORMAL throw
python3 tune.py special --zero-y -40   # special is an unverified starting point
python3 tune.py normal                # inspect existing values
python3 tune.py normal --dot 2 45     # move ONE mark: index 2 -> 45px BELOW zero
python3 tune.py normal --dots "0,19,43,76,117,166"
python3 tune.py special --stretch 0.9
```

Each change appears without restarting the overlay. `--zero-y` is independent for normal and special, and `--center-y` is reserved for visual alignment with Sober's actual viewport.

**Simple no-studs test:** stand still, place a visible target on the zero dot, and throw normally. If the spear lands below it, put the target on the FIRST lower dot and try again from the same spot. Adjust that dot's offset with `--dot 1 NUMBER` until it hits. Then back up and repeat with a farther dot. Repeat independently for the special ability. The footage's release animations are not used for this calibration.

The lower dots are aiming references, NOT proven distances. A stationary target, unchanged FOV/resolution, and impact marks help. Since target distance isn't measured, the marks won't correspond to known studs until a separate distance reference is available.

**Mouse safety:** The new overlay uses an empty GDK input region in addition to pass-through. If your compositor still captures input, press Ctrl+C in its terminal. This KDE + Sober combination still requires device testing.
