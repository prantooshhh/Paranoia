"""
rendering/visibility.py
Computes the set of map grid cells visible to the player
from their current position within a forward-facing cone.
"""

from __future__ import annotations
import math
from typing import TYPE_CHECKING

from paranoia.map_data   import GAME_MAP
from paranoia.constants  import VIEW_CONE_ANGLE

if TYPE_CHECKING:
    from paranoia.entities.player import Player


def find_cone_blocks(
    x: int,
    y: int,
    dir_angle: float,
    player: Player,
) -> set[tuple[int, int]]:
    """
    Return the set of (i, j) grid cells visible from (x, y)
    within a VIEW_CONE_ANGLE-degree cone pointing in dir_angle.

    Cells are excluded if a wall lies along the line of sight.
    """
    visible: set[tuple[int, int]] = set()

    rad = math.radians(dir_angle - 45)
    fx  = math.cos(rad)
    fy  = math.sin(rad)

    half_cone = math.radians(VIEW_CONE_ANGLE / 2)
    r         = player.view_range_active

    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            # Always include the player's own cell
            if dx == 0 and dy == 0:
                visible.add((x, y))
                continue

            dist_sq = dx * dx + dy * dy
            if dist_sq > r * r:
                continue

            dist  = math.sqrt(dist_sq)
            vx    = dx / dist
            vy    = dy / dist
            dot   = fx * vx + fy * vy
            angle = math.acos(max(-1.0, min(1.0, dot)))

            if angle > half_cone:
                continue

            # Ray-march to check for wall occlusion
            steps          = int(dist)
            sight_blocked  = False
            for step in range(1, steps + 1):
                bx = int(x + vx * step)
                by = int(y + vy * step)
                if 0 <= bx < len(GAME_MAP) and 0 <= by < len(GAME_MAP):
                    if GAME_MAP[bx][by] == 1:
                        sight_blocked = True
                        break

            if not sight_blocked:
                visible.add((x + dx, y + dy))

    return visible
