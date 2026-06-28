# -*- coding: utf-8 -*-
"""Appearance page – allows the user to tweak visual aspects of the desktop.

Only a subset of the settings described in the specification are implemented
here.  Each widget writes its value back to the JSON backend immediately.
"""

from __future__ import annotations

from pathlib import Path

from gi.repository import Gtk, Gdk, Gio

from backend.config import Config
from widgets.card import SettingsCard
from widgets.setting_row import SettingsRow


class AppearancePage(Gtk.Box):
    """Page that edits appearance‑related configuration values."""

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_start=12, margin_end=12, margin_top=12, margin_bottom=12)

        # Load (or create) the appearance configuration file.
        default_cfg = {
            "dark_mode": False,
            "accent_color": "#3584e4",
            "wallpaper": "",
            "transparency": 0.0,
            "animations": True,
            "icon_theme": "default",
            "font": "Sans 11",
            "cursor_theme": "default",
            "corner_radius": 4,
        }
        self._cfg = Config("appearance", default_cfg)

        card = SettingsCard(title="Appearance")
        self.append(card)

        # Dark mode ----------------------------------------------------------
        dark_switch = Gtk.Switch()
        dark_switch.set_active(bool(self._cfg.get("dark_mode", False)))
        dark_switch.connect("state-set", self._on_dark_mode_toggled)
        card.add(SettingsRow("Dark mode", widget=dark_switch))

        # Accent colour ------------------------------------------------------
        accent_entry = Gtk.Entry()
        accent_entry.set_text(str(self._cfg.get("accent_color", "#3584e4")))
        accent_entry.set_placeholder_text("#RRGGBB")
        accent_entry.connect("changed", self._on_accent_changed)
        card.add(SettingsRow("Accent colour", widget=accent_entry))

        # Wallpaper ----------------------------------------------------------
        wallpaper_button = Gtk.Button(label="Select wallpaper")
        wallpaper_button.connect("clicked", self._on_wallpaper_clicked)
        card.add(SettingsRow("Wallpaper", widget=wallpaper_button))

        # Transparency slider -------------------------------------------------
        transparency_adj = Gtk.Adjustment(value=float(self._cfg.get("transparency", 0.0)), lower=0.0, upper=1.0, step_increment=0.05)
        transparency_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=transparency_adj)
        transparency_scale.set_digits(2)
        transparency_scale.set_hexpand(True)
        transparency_scale.connect("value-changed", self._on_transparency_changed)
        card.add(SettingsRow("Transparency", widget=transparency_scale))

    # ---------------------------------------------------------------------
    # Signal callbacks – each writes back to the JSON config immediately.
    # ---------------------------------------------------------------------
    def _on_dark_mode_toggled(self, switch: Gtk.Switch, state: bool) -> bool:
        self._cfg.set("dark_mode", state)
        return False  # allow further processing

    def _on_accent_changed(self, entry: Gtk.Entry) -> None:
        self._cfg.set("accent_color", entry.get_text())

    def _on_wallpaper_selected(self, chooser: Gtk.FileChooserButton) -> None:
        file = chooser.get_file()
        if file:
            self._cfg.set("wallpaper", file.get_path())

    def _on_transparency_changed(self, scale: Gtk.Scale) -> None:
        self._cfg.set("transparency", scale.get_value())

    def _on_wallpaper_clicked(self, button: Gtk.Button) -> None:
        """Open a file chooser to select a wallpaper and store its path."""
        dialog = Gtk.FileChooserNative(
            title="Select Wallpaper",
            transient_for=self.get_root(),
            modal=True,
            action=Gtk.FileChooserAction.OPEN,
        )
        # Filter to image files (optional)
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Image files")
        filter_img.add_mime_type("image/*")
        dialog.add_filter(filter_img)
        if hasattr(dialog, 'run'):
            response = dialog.run()
            if response == Gtk.ResponseType.ACCEPT:
                file_obj = dialog.get_file()
                if file_obj:
                    file_path = file_obj.get_path()
                    self._cfg.set("wallpaper", file_path)
            dialog.destroy()
        else:
            dialog.show()
            dialog.destroy()
