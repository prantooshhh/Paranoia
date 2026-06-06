"""
rendering/world.py
Draws the visible portion of the game map: floor tiles and walls.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
from OpenGL.GL   import *
from OpenGL.GLUT import *

from paranoia.constants         import GRID_LENGTH
from paranoia.map_data          import GAME_MAP
from paranoia.rendering.camera  import color_func

if TYPE_CHECKING:
    from paranoia.entities.player import Player


def draw_map(player: Player) -> None:
    """Render every active map cell visible to the player."""
    for i in range(len(player.active_blocks)):
        for j in range(len(player.active_blocks)):
            if not player.active_blocks[i][j]:
                continue
            if GAME_MAP[i][j] == 1:
                draw_wall(i, j, player)
            elif GAME_MAP[i][j] == 2:
                draw_block(i, j, player)


def draw_wall(i: int, j: int, player: Player) -> None:
    """Draw a single wall cube at grid position (i, j)."""
    x = (i - len(GAME_MAP) // 2) * GRID_LENGTH
    y = (j - len(GAME_MAP) // 2) * GRID_LENGTH

    glPushMatrix()
    glTranslatef(x + 25, y - 25, 80)
    glScalef(1, 1, 4)
    glColor3f(*color_func(x + 25, y - 25, 1, 1, 1, player))
    glutSolidCube(50)
    glPopMatrix()



