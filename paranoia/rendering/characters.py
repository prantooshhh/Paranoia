"""
rendering/characters.py
Renders the local player model and remote opponent (creature) models.
"""

from __future__ import annotations
import math
import random
from time import time
from typing import TYPE_CHECKING

from OpenGL.GL   import *
from OpenGL.GLU  import *
from OpenGL.GLUT import *

if TYPE_CHECKING:
    from paranoia.entities.player import Player


# ── Helpers ────────────────────────────────────────────────────────────────

def _draw_cube(w: float, h: float, d: float, color: tuple) -> None:
    """Scale and draw a unit solid cube with the given dimensions and colour."""
    glPushMatrix()
    glScalef(w, h, d)
    glColor3f(*color)
    glutSolidCube(1.0)
    glPopMatrix()


# ── Player ─────────────────────────────────────────────────────────────────

def draw_player(player: Player, game_over: bool, gun_fired: bool) -> None:
    """Render the local player's character model."""
    glPushMatrix()

    if game_over:
        glRotatef(90, 0, 1, 0)

    glTranslatef(player.x, player.y, player.z + 50)
    glRotatef(player.angle, 0, 0, 1)
    glScalef(40, 40, 40)

    # Torso
    glPushMatrix()
    glTranslatef(0, 0, 1)
    _draw_cube(1.0, 0.5, 1.5, (0.0, 0.4, 0.2))
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 0, 2.4)
    _draw_cube(0.8, 0.8, 0.8, (1.0, 0.8, 0.6))
    glPopMatrix()

    # Eyes
    glPushMatrix()
    glTranslatef(0, -0.45, 2.5)
    glPushMatrix()
    glTranslatef(-0.2, 0, 0)
    _draw_cube(0.15, 0.05, 0.05, (0, 0, 0))
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.2, 0, 0)
    _draw_cube(0.15, 0.05, 0.05, (0, 0, 0))
    glPopMatrix()
    glPopMatrix()

    # Hair
    glPushMatrix()
    glTranslatef(0, 0, 2.9)
    glScalef(1.0, 1.0, 0.3)
    _draw_cube(0.75, 0.75, 0.75, (0.0, 0.0, 0.0))
    glPopMatrix()

    # Right arm + gun
    glPushMatrix()
    glTranslatef(-0.65, 0, 1.9)
    glRotatef(-80, 1, 0, 0)
    glRotatef(10, 0, 1, 0)
    _draw_cube(0.4, 0.4, 1.4, (1.0, 0.8, 0.6))

    glPushMatrix()
    glTranslatef(0, -0.1, -1.5)
    glRotatef(10, 0, 1, 0)
    glColor3f(0.3, 0.3, 0.3)
    gluCylinder(gluNewQuadric(), 0.05, 0.1, 0.8, 8, 2)

    if gun_fired:
        glPushMatrix()
        glTranslate(0, 0, -0.2)
        s = 0.2 + random.uniform(-0.2, 0.2)
        glScalef(s, s, s)
        glColor3f(1.0, 1.0, 0.0)
        glutSolidCone(0.5, 1.0, 12, 12)
        glPopMatrix()

    glPopMatrix()
    glPopMatrix()

    # Left arm + torch
    glPushMatrix()
    glTranslatef(0.65, 0, 1.9)
    glRotatef(30, 1, 0, 0)
    _draw_cube(0.4, 0.4, 1.4, (1.0, 0.8, 0.6))

    glPushMatrix()
    glTranslatef(0, 0, 0.2)
    glRotatef(-10, 0, 0, 1)
    glColor3f(0.5, 0.25, 0.1)
    gluCylinder(gluNewQuadric(), 0.1, 0.1, 1.2, 8, 8)

    # Legs
    glPushMatrix()
    glTranslatef(-0.35, 0, -0.4)
    _draw_cube(0.4, 0.4, 1.4, (0.2, 0.1, 0.6))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.4, 0, -0.4)
    _draw_cube(0.4, 0.4, 1.4, (0.2, 0.1, 0.6))
    glPopMatrix()

    glPopMatrix()
