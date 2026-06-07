"""
ui/minimap.py
Draws the minimap overlay in the bottom-right corner of the screen.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from OpenGL.GL  import *
from OpenGL.GLU import *

from paranoia.constants import GRID_LENGTH
from paranoia.map_data  import GAME_MAP

if TYPE_CHECKING:
    from paranoia.entities.player  import Player
    from paranoia.entities.powerup import Powerup

_MINIMAP_SIZE   = 150   # pixel dimensions of the minimap viewport
_ORTHO_SIZE     = 200   # ortho units matching the minimap space


def draw_minimap(
    width: int,
    height: int,
    player: Player,
    powerups: list[Powerup],
) -> None:
    """Render the minimap into a corner viewport, then restore the main viewport."""
    glViewport(width - _MINIMAP_SIZE, 0, _MINIMAP_SIZE, _MINIMAP_SIZE)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, _ORTHO_SIZE, 0, _ORTHO_SIZE)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    # Background
    glColor3f(0.05, 0.05, 0.05)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(_ORTHO_SIZE, 0)
    glVertex2f(_ORTHO_SIZE, _ORTHO_SIZE)
    glVertex2f(0, _ORTHO_SIZE)
    glEnd()

    # Wall cells
    n         = len(GAME_MAP)
    cell_size = _ORTHO_SIZE / n
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    for i in range(n):
        for j in range(n):
            if GAME_MAP[i][j] == 1:
                x = i * cell_size
                y = j * cell_size
                glVertex2f(x, y)
                glVertex2f(x + cell_size, y)
                glVertex2f(x + cell_size, y + cell_size)
                glVertex2f(x, y + cell_size)
    glEnd()

    # Player dot (red)
    px = int(player.x // GRID_LENGTH + n // 2) * cell_size
    py = int(player.y // GRID_LENGTH + n // 2) * cell_size
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(px - 3, py - 3)
    glVertex2f(px + 3, py - 3)
    glVertex2f(px + 3, py + 3)
    glVertex2f(px - 3, py + 3)
    glEnd()

    # Powerup dots
    for p in powerups:
        if p.taken:
            continue
        mx = int(p.x // GRID_LENGTH + n // 2) * cell_size
        my = int(p.y // GRID_LENGTH + n // 2) * cell_size
        if p.type == "speed":
            glColor3f(0.0, 1.0, 0.0)
        elif p.type == "range":
            glColor3f(1.0, 1.0, 0.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(mx - 2, my - 2)
        glVertex2f(mx + 2, my - 2)
        glVertex2f(mx + 2, my + 2)
        glVertex2f(mx - 2, my + 2)
        glEnd()

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glViewport(0, 0, width, height)
