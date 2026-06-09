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

    # Torch flame
    glTranslatef(0, 0, 1.2)
    t              = time()
    base_scale     = 0.25
    flicker1       = 0.10 * math.sin(t * 8.0)
    flicker2       = 0.08 * math.sin(t * 6.3)
    flicker3       = 0.05 * math.sin(t * 4.7)

    glPushMatrix()
    glScalef(base_scale, base_scale, base_scale + flicker3)
    glColor3f(1.0, 0.5, 0.0)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 0.1)
    inner = base_scale * 0.6 + flicker2 * 0.4 + flicker3 * 0.4
    glScalef(inner, inner, inner + flicker1 * 0.3)
    glColor3f(1.0, 0.2, 0.0)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()
    glPopMatrix()

    glColor3f(1.0, 0.5, 0.0)
    glutSolidCube(0.4)

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


# ── Creature (remote opponents) ────────────────────────────────────────────

def draw_creature(
    x: float,
    y: float,
    z: float,
    alive: bool,
    player: Player,
) -> None:
    """Render a remote opponent's creature model, facing the local player."""
    glPushMatrix()

    ang = math.degrees(math.atan2(player.y - y, player.x - x)) + 90
    if not alive:
        glRotatef(90, 0, 1, 0)
    glTranslatef(x, y, z)
    glRotatef(ang, 0, 0, 1)
    glScalef(1.3, 1.3, 1.3)

    # Body
    glPushMatrix()
    glTranslatef(0, 0, 90)
    glScalef(30, 20, 60)
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 0, 135)
    glScalef(25, 25, 25)
    glColor3f(0.15, 0.15, 0.15)
    glutSolidCube(1)
    glPopMatrix()

    # Left eye
    glPushMatrix()
    glTranslatef(-8, -15, 135)
    glScalef(4, 2, 4)
    glColor3f(1.0, 0.0, 0.0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Right eye
    glPushMatrix()
    glTranslatef(8, -15, 135)
    glScalef(4, 2, 4)
    glColor3f(1.0, 0.0, 0.0)
    glutSolidCube(1.0)
    glPopMatrix()

    # Left arm
    glPushMatrix()
    glTranslatef(-20, 0, 80)
    glScalef(8, 8, 70)
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()

    # Right arm
    glPushMatrix()
    glTranslatef(20, 0, 80)
    glScalef(8, 8, 70)
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()

    # Left leg
    glPushMatrix()
    glTranslatef(-8, 0, 30)
    glScalef(8, 8, 60)
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(8, 0, 30)
    glScalef(8, 8, 60)
    glColor3f(0.1, 0.1, 0.1)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()
