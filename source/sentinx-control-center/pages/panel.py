# -*- coding: utf-8 -*-
"""Panel page – currently a placeholder for future implementation.
"""

from __future__ import annotations

from gi.repository import Gtk


class PanelPage(Gtk.Box):
    """Placeholder page that will eventually host panel configuration UI."""

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_start=12, margin_end=12, margin_top=12, margin_bottom=12)
        label = Gtk.Label(label="Panel configuration will be added here.")
        label.set_margin_top(24)
        self.append(label)
