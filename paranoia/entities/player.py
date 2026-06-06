"""
entities/player.py
Local player entity: state, movement, collision, and vision cone.
"""

from __future__ import annotations

import math
import numpy as np

from paranoia.constants import (
    GRID_LENGTH, MAP_SIZE,
    BASE_SPEED, BASE_VIEW_RANGE, BASE_VIEW_RANGE_ACTIVE,
    ROTATION_SPEED,
    SPEED_BOOST, SPEED_MAX, RANGE_BOOST, RANGE_ACTIVE_BOOST,
)
from paranoia.map_data import GAME_MAP
from paranoia.rendering.visibility import find_cone_blocks


class Player:
    """The locally-controlled player character."""

    def __init__(self, ip: str, start_pos: list[int]) -> None:
        self.ip    = ip
        self.angle = 0.0

        # World-space position
        self.x = (start_pos[0] - MAP_SIZE // 2) * GRID_LENGTH
        self.y = (start_pos[1] - MAP_SIZE // 2) * GRID_LENGTH
        self.z = 0.0

        # Stats
        self.speed             = BASE_SPEED
        self.view_range        = BASE_VIEW_RANGE
        self.view_range_active = BASE_VIEW_RANGE_ACTIVE

        # Inventory / state
        self.powerups: list[str]      = []
        self.powerups_name: list[str] = []
        self.killed: list[str]        = []
        self.alive     = True
        self.reloading = False

        # Computed visibility grid — updated on every move/rotation
        self.active_blocks = np.zeros((MAP_SIZE, MAP_SIZE), dtype=np.float32)
        self._update_active_blocks()

    # ── Movement ─────────────────────────────────────────────────────────────

    def rotate_left(self, dt: float) -> None:
        self.angle += ROTATION_SPEED * dt
        self._update_active_blocks()

    def rotate_right(self, dt: float) -> None:
        self.angle -= ROTATION_SPEED * dt
        self._update_active_blocks()

    def go_forward(self, dt: float) -> None:
        self._move(dt, direction=1)

    def go_backward(self, dt: float) -> None:
        self._move(dt, direction=-1)

    def _move(self, dt: float, direction: int) -> None:
        """Shared movement logic for forward and backward travel."""
        rad    = math.radians(self.angle - 90)
        next_x = self.x + direction * math.cos(rad) * self.speed * dt
        next_y = self.y + direction * math.sin(rad) * self.speed * dt

        # Collision offset differs slightly between forward and backward
        offset = 50 if direction == 1 else 25

        n = MAP_SIZE
        next_i  = int(next_x // GRID_LENGTH + n // 2)
        next_j  = int(next_y // GRID_LENGTH + n // 2) + 1

        next_i_plus  = int((next_x + offset) // GRID_LENGTH + n // 2)
        next_j_plus  = int((next_y + offset) // GRID_LENGTH + n // 2) + 1
        next_i_minus = int((next_x - offset) // GRID_LENGTH + n // 2)
        next_j_minus = int((next_y - offset) // GRID_LENGTH + n // 2) + 1

        if GAME_MAP[next_i_plus][next_j] != 1 and GAME_MAP[next_i_minus][next_j] != 1:
            self.x = next_x
        if GAME_MAP[next_i][next_j_plus] != 1 and GAME_MAP[next_i][next_j_minus] != 1:
            self.y = next_y

        self._update_active_blocks()

    # ── Vision ───────────────────────────────────────────────────────────────

    def _update_active_blocks(self) -> None:
        """
        Recompute which map cells are visible to the player.

        Values written to self.active_blocks:
            0 — not rendered (out of range or behind player)
            1 — rendered but outside the vision cone (ambient surroundings)
            2 — rendered and inside the vision cone (lit area)
        """
        n       = MAP_SIZE
        px, py  = int(self.x), int(self.y)
        p_angle = (self.angle - 45) % 360
        pxi     = int(px // GRID_LENGTH + n // 2)
        pyi     = int(py // GRID_LENGTH + n // 2)

        self.active_blocks = np.zeros((n, n), dtype=np.float32)

        # Always render a square neighbourhood regardless of cone
        r = 17
        self.active_blocks[
            max(pxi - r, 0):min(pxi + r + 1, n),
            max(pyi - r, 0):min(pyi + r + 1, n),
        ] = 1

        # Lit cone blocks
        for i, j in find_cone_blocks(pxi, pyi, p_angle, self):
            if 0 <= i < n and 0 <= j < n:
                self.active_blocks[i, j] = 2

    # ── Gun ──────────────────────────────────────────────────────────────────

    def reload(self) -> None:
        """Called by a timer thread after the reload delay."""
        self.reloading = False
