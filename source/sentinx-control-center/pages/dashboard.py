# -*- coding: utf-8 -*-
"""Dashboard page – provides a quick overview of system status.

For now the page displays static placeholder values; the design mirrors the
layout of a typical GNOME Settings dashboard and can be expanded later.
"""

from __future__ import annotations

from gi.repository import Gtk

from widgets.card import SettingsCard
from widgets.setting_row import SettingsRow


class DashboardPage(Gtk.Box):
    """Container for the dashboard overview cards."""

    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_start=12, margin_end=12, margin_top=12, margin_bottom=12)

        # CPU usage card
        cpu_card = SettingsCard(title="CPU")
        cpu_card.add(SettingsRow("Model", subtitle="Intel Core i7-12700H"))
        cpu_card.add(SettingsRow("Usage", subtitle="12 %"))
        self.append(cpu_card)

        # RAM usage card
        ram_card = SettingsCard(title="Memory")
        ram_card.add(SettingsRow("Total", subtitle="16 GB"))
        ram_card.add(SettingsRow("Used", subtitle="4 GB (25 %)"))
        self.append(ram_card)

        # GPU card
        gpu_card = SettingsCard(title="GPU")
        gpu_card.add(SettingsRow("Model", subtitle="NVIDIA RTX 3060"))
        gpu_card.add(SettingsRow("Usage", subtitle="8 %"))
        self.append(gpu_card)

        # Storage card
        storage_card = SettingsCard(title="Storage")
        storage_card.add(SettingsRow("Root", subtitle="256 GB SSD – 78 % used"))
        storage_card.add(SettingsRow("Home", subtitle="1 TB HDD – 45 % used"))
        self.append(storage_card)

        # Battery card
        battery_card = SettingsCard(title="Battery")
        battery_card.add(SettingsRow("Charge", subtitle="85 %"))
        battery_card.add(SettingsRow("State", subtitle="Discharging"))
        self.append(battery_card)

        # Dock status card
        dock_card = SettingsCard(title="Dock")
        dock_card.add(SettingsRow("Pinned apps", subtitle="5"))
        dock_card.add(SettingsRow("Position", subtitle="Bottom"))
        self.append(dock_card)

        # Sentinel status card
        sentinel_card = SettingsCard(title="Sentinel AI")
        sentinel_card.add(SettingsRow("Status", subtitle="Idle"))
        self.append(sentinel_card)

        # Updates card
        updates_card = SettingsCard(title="Updates")
        updates_card.add(SettingsRow("Pending", subtitle="2 packages"))
        self.append(updates_card)
