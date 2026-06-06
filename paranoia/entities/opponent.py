"""
entities/opponent.py
Remote player state received from the network.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from paranoia.entities.player  import Player
    from paranoia.entities.powerup import Powerup


class Opponent:
    """Represents a single remote player."""

    def __init__(self, ip: str) -> None:
        self.ip            = ip
        self.x: float      = 0.0
        self.y: float      = 0.0
        self.powerups_name: list[str] = []
        self.killed: list[str]        = []
        self.alive: bool   = True

    def update(
        self,
        x: float,
        y: float,
        powerups_name: list[str],
        killed: list[str],
        alive: bool,
        *,
        powerups: list[Powerup],
        local_player: Player,
        all_opponents: list[Opponent],
    ) -> None:
        """Apply a state packet received from the server."""
        self.x             = x
        self.y             = y
        self.powerups_name = powerups_name
        self.killed        = killed
        self.alive         = alive

        # Mark powerups as taken if this opponent collected them
        for p in powerups:
            if p.name in powerups_name:
                p.taken = True

        # Apply kill events to all entities
        for killed_ip in killed:
            if local_player.ip in killed:
                local_player.alive = False
            for opp in all_opponents:
                if opp.ip == killed_ip:
                    opp.alive = False
