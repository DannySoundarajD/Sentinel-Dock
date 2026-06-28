# -*- coding: utf-8 -*-
"""Developer page – provides debugging tools, logs and experimental features.
"""

from __future__ import annotations

from gi.repository import Gtk


class DeveloperPage(Gtk.Box):
    """Placeholder page for developer utilities."""

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_start=12, margin_end=12, margin_top=12, margin_bottom=12)
        label = Gtk.Label(label="Developer utilities (logs, plugins, experimental flags) will appear here.")
        label.set_margin_top(24)
        self.append(label)
