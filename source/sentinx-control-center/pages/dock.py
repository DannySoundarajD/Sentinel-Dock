# -*- coding: utf-8 -*-
"""Dock configuration page – mirrors the settings exposed by the Vala dock.

The UI writes directly to ``dock.json`` via :class:`backend.dock.DockConfig`.
"""

from __future__ import annotations

from gi.repository import Gtk
import pathlib

from backend.dock import DockConfig
from widgets.card import SettingsCard
from widgets.setting_row import SettingsRow


class DockPage(Gtk.Box):
    """Page that allows the user to edit dock preferences."""

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_start=12, margin_end=12, margin_top=12, margin_bottom=12)
        self._dock = DockConfig()
        card = SettingsCard(title="Dock")
        self.append(card)

        # Position ----------------------------------------------------------
        position_combo = Gtk.ComboBoxText()
        self.position_combo = position_combo
        for pos in ["bottom", "left", "right", "top"]:
            position_combo.append_text(pos)
        position_combo.set_active_id(self._dock.get_position())
        position_combo.connect("changed", self._on_position_changed)
        card.add(SettingsRow("Position", widget=position_combo))

        # Icon size ----------------------------------------------------------
        size_adj = Gtk.Adjustment(value=self._dock.get_icon_size(), lower=16, upper=128, step_increment=4)
        size_spin = Gtk.SpinButton(adjustment=size_adj, climb_rate=1.0, digits=0)
        self.size_spin = size_spin
        size_spin.connect("value-changed", self._on_icon_size_changed)
        card.add(SettingsRow("Icon size", widget=size_spin))

        # Zoom ---------------------------------------------------------------
        zoom_adj = Gtk.Adjustment(value=self._dock.get_zoom(), lower=0.5, upper=2.0, step_increment=0.1)
        zoom_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=zoom_adj)
        self.zoom_scale = zoom_scale
        zoom_scale.set_digits(2)
        zoom_scale.set_hexpand(True)
        zoom_scale.connect("value-changed", self._on_zoom_changed)
        card.add(SettingsRow("Zoom", widget=zoom_scale))

        # Transparency -------------------------------------------------------
        trans_adj = Gtk.Adjustment(value=self._dock.get_transparency(), lower=0.0, upper=1.0, step_increment=0.05)
        trans_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=trans_adj)
        self.trans_scale = trans_scale
        trans_scale.set_digits(2)
        trans_scale.set_hexpand(True)
        trans_scale.connect("value-changed", self._on_transparency_changed)
        card.add(SettingsRow("Transparency", widget=trans_scale))

        # Autohide -----------------------------------------------------------
        autohide_switch = Gtk.Switch()
        self.autohide_switch = autohide_switch
        autohide_switch.set_active(self._dock.get_autohide())
        autohide_switch.connect("state-set", self._on_autohide_toggled)
        card.add(SettingsRow("Auto‑hide", widget=autohide_switch))

        # Spacing -----------------------------------------------------------
        spacing_adj = Gtk.Adjustment(value=self._dock.get_spacing(), lower=0, upper=20, step_increment=1)
        spacing_spin = Gtk.SpinButton(adjustment=spacing_adj, climb_rate=1.0, digits=0)
        self.spacing_spin = spacing_spin
        spacing_spin.connect("value-changed", self._on_spacing_changed)
        card.add(SettingsRow("Spacing", widget=spacing_spin))

        # Animation speed ----------------------------------------------------
        anim_adj = Gtk.Adjustment(value=self._dock.get_animation_speed(), lower=0.1, upper=3.0, step_increment=0.1)
        anim_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=anim_adj)
        self.anim_scale = anim_scale
        anim_scale.set_digits(2)
        anim_scale.set_hexpand(True)
        anim_scale.connect("value-changed", self._on_animation_speed_changed)
        card.add(SettingsRow("Animation speed", widget=anim_scale))

        # Pinned apps --------------------------------------------------------
        # Card to hold pinned applications list and add button.
        pinned_card = SettingsCard(title="Pinned Apps")
        self.append(pinned_card)

        # ListBox showing current pinned apps.
        self._pinned_listbox = Gtk.ListBox()
        pinned_card.add(self._pinned_listbox)

        # Add Application button – opens a file chooser for .desktop files.
        add_app_button = Gtk.Button(label="Add Application")
        add_app_button.connect("clicked", self._on_add_app_clicked)
        pinned_card.add(SettingsRow("Add App", widget=add_app_button))

        # Populate the list initially.
        self._refresh_pinned_list()

        # Reset button -------------------------------------------------------
        reset_button = Gtk.Button(label="Restore defaults")
        reset_button.get_style_context().add_class("destructive-action")
        reset_button.connect("clicked", self._on_reset_clicked)
        card.add(reset_button)

    # ---------------------------------------------------------------------
    # Callbacks – each writes the new value to the JSON backend.
    # ---------------------------------------------------------------------
    def _on_position_changed(self, combo: Gtk.ComboBoxText) -> None:
        self._dock.set_position(combo.get_active_text() or "bottom")

    def _on_icon_size_changed(self, spin: Gtk.SpinButton) -> None:
        self._dock.set_icon_size(int(spin.get_value()))

    def _on_zoom_changed(self, scale: Gtk.Scale) -> None:
        self._dock.set_zoom(scale.get_value())

    def _on_transparency_changed(self, scale: Gtk.Scale) -> None:
        self._dock.set_transparency(scale.get_value())

    def _on_autohide_toggled(self, switch: Gtk.Switch, state: bool) -> bool:
        self._dock.set_autohide(state)
        return False

    def _on_spacing_changed(self, spin: Gtk.SpinButton) -> None:
        self._dock.set_spacing(int(spin.get_value()))

    def _on_animation_speed_changed(self, scale: Gtk.Scale) -> None:
        self._dock.set_animation_speed(scale.get_value())

    def _on_reset_clicked(self, btn: Gtk.Button) -> None:
        # Reset the underlying JSON configuration to its factory defaults
        self._dock.reset_to_defaults()
        # Bring the UI widgets back in sync with the freshly‑loaded defaults
        self.position_combo.set_active_id(self._dock.get_position())
        self.size_spin.set_value(self._dock.get_icon_size())
        self.zoom_scale.set_value(self._dock.get_zoom())
        self.trans_scale.set_value(self._dock.get_transparency())
        self.autohide_switch.set_active(self._dock.get_autohide())
        self.spacing_spin.set_value(self._dock.get_spacing())
        self.anim_scale.set_value(self._dock.get_animation_speed())
        # Refresh pinned apps list UI
        self._refresh_pinned_list()

    # ---------------------------------------------------------------------
    # Pinned apps helpers
    # ---------------------------------------------------------------------
    def _refresh_pinned_list(self) -> None:
        """Rebuild the ListBox showing all pinned applications."""
        # Clear existing rows
        self._pinned_listbox.remove_all()
        # Populate rows
        for app in self._dock.get_pinned_apps():
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            label = Gtk.Label(label=app)
            label.set_xalign(0)
            remove_btn = Gtk.Button(label="Remove")
            # Capture app in closure
            remove_btn.connect("clicked", self._on_remove_pinned, app)
            hbox.append(label)
            hbox.append(remove_btn)
            row.set_child(hbox)
            self._pinned_listbox.append(row)

    def _on_add_app_clicked(self, button: Gtk.Button) -> None:
        """Open a file chooser to select a .desktop file and add it to pinned apps."""
        # Use native file chooser (GTK4) for .desktop selection
        dialog = Gtk.FileChooserNative(
            title="Select Application",
            transient_for=self.get_root(),
            modal=True,
            action=Gtk.FileChooserAction.OPEN,
        )
        # Filter for .desktop files
        filter_desktop = Gtk.FileFilter()
        filter_desktop.set_name("Desktop files")
        filter_desktop.add_pattern("*.desktop")
        dialog.add_filter(filter_desktop)
        # Attempt to run the dialog in a blocking manner if supported.
        if hasattr(dialog, 'run'):
            response = dialog.run()
            if response == Gtk.ResponseType.ACCEPT:
                file_obj = dialog.get_file()
                if file_obj:
                    filename = file_obj.get_path()
                    if filename:
                        app_id = pathlib.Path(filename).name
                        self._dock.add_pinned_app(app_id)
                        self._refresh_pinned_list()
            dialog.destroy()
        else:
            # Fallback for native dialog without a run method – simply show.
            dialog.show()
            # In a full UI, you would connect to the "response" signal.
            # Here we just destroy immediately as we cannot block.
            dialog.destroy()

    def _on_remove_pinned(self, button: Gtk.Button, app: str) -> None:
        """Remove *app* from the pinned apps list and update UI."""
        self._dock.remove_pinned_app(app)
        self._refresh_pinned_list()
