# -*- coding: utf-8 -*-
"""Row widget used inside a :class:`~widgets.card.SettingsCard`.

It is based on :class:`Adw.ActionRow` which nicely aligns a title on the left
and an arbitrary widget (switch, slider, dropdown, etc.) on the right.
"""

from __future__ import annotations

from gi.repository import Gtk


class SettingsRow(Gtk.Box):
    """A row that holds a label and an optional trailing widget.

    Parameters
    ----------
    title:
        The primary text displayed on the left.
    subtitle:
        Optional secondary text displayed under the title.
    widget:
        A :class:`Gtk.Widget` that will be attached to the end of the row.
    """

    def __init__(self, title: str, subtitle: str | None = None, widget: Gtk.Widget | None = None) -> None:
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        title_label = Gtk.Label(label=title)
        title_label.set_xalign(0)
        self.append(title_label)
        if subtitle:
            subtitle_label = Gtk.Label(label=subtitle)
            subtitle_label.set_xalign(0)
            self.append(subtitle_label)
        if widget:
            self.append(widget)
            widget.show()
