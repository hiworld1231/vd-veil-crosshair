#!/usr/bin/env python3
"""Click-through KDE Plasma Wayland overlay for The Veil."""
from __future__ import annotations

import os
import sys

if os.environ.get("XDG_SESSION_TYPE", "").lower() != "wayland":
    sys.exit("This overlay requires a Wayland session. Use PNG export instead on X11.")

try:
    import cairo
    import gi
    gi.require_version("Gtk", "3.0")
    gi.require_version("Gdk", "3.0")
    gi.require_version("GtkLayerShell", "0.1")
    from gi.repository import Gtk, Gdk, GLib, GtkLayerShell
except (ImportError, ValueError) as err:
    sys.exit("Install: sudo pacman -S --needed python-gobject python-cairo gtk3 gtk-layer-shell\n" + str(err))

from reticle import config_path, load_config, paint


class Overlay(Gtk.Window):
    def __init__(self):
        super().__init__(title="VD Veil Crosshair")
        self.config = load_config()
        self.config_stamp = None
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_accept_focus(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_default_size(1, 1)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_namespace(self, "vd-veil-crosshair")
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.NONE)
        GtkLayerShell.set_exclusive_zone(self, 0)
        for edge in (GtkLayerShell.Edge.TOP, GtkLayerShell.Edge.BOTTOM,
                     GtkLayerShell.Edge.LEFT, GtkLayerShell.Edge.RIGHT):
            GtkLayerShell.set_anchor(self, edge, True)

        self.canvas = Gtk.DrawingArea()
        self.canvas.set_app_paintable(True)
        self.canvas.connect("draw", self.draw)
        self.add(self.canvas)
        self.connect("realize", self.on_realize)
        self.connect("map-event", self.on_map_event)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        GLib.timeout_add(350, self.poll_config)

    def apply_click_through(self):
        """Give the Wayland surface an EMPTY input region.

        set_pass_through() alone isn't enough for a top-level layer-shell
        window: it can still eat mouse motion/clicks over another process.
        An empty cairo.Region is forwarded to the compositor as a
        zero-area wl_surface input region.
        """
        window = self.get_window()
        if window is None:
            return False
        try:
            empty = cairo.Region()
            self.input_shape_combine_region(empty)
            window.input_shape_combine_region(empty, 0, 0)
            window.set_pass_through(True)
        except Exception as exc:
            print(f"Cannot make overlay click-through: {exc}", file=sys.stderr)
            self.destroy()  # Fail closed: never leave a fullscreen input blocker.
        return False

    def on_realize(self, *_):
        self.apply_click_through()

    def on_map_event(self, *_):
        # Some backends replace their input region as the surface is mapped.
        GLib.idle_add(self.apply_click_through)
        return False

    def draw(self, widget, ctx):
        allocation = widget.get_allocation()
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.paint()
        ctx.restore()
        paint(ctx, self.config, allocation.width, allocation.height)
        return False

    def poll_config(self):
        try:
            stamp = config_path().stat().st_mtime_ns
            if stamp != self.config_stamp:
                next_config = load_config()
                if next_config.get("active_profile") not in next_config.get("profiles", {}):
                    raise ValueError("Invalid active_profile")
                self.config = next_config
                self.config_stamp = stamp
                self.canvas.queue_draw()
        except (OSError, ValueError, KeyError) as exc:
            print(f"Config unchanged: {exc}", file=sys.stderr)
        return True


def main():
    if not GtkLayerShell.is_supported():
        sys.exit("Layer-shell protocol unavailable. Switch to KDE Plasma Wayland or use PNG export.")
    Overlay()
    Gtk.main()


if __name__ == "__main__":
    main()
