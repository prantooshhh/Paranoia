"""
rendering/powerups_renderer.py
Renders powerup pickup objects in world space.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from OpenGL.GL   import *
from OpenGL.GLUT import *
from OpenGL.GLU  import *

if TYPE_CHECKING:
    from paranoia.entities.powerup import Powerup


def draw_powerup(p: Powerup) -> None:
    """Render a single powerup at its world position."""
    glPushMatrix()
    glTranslatef(p.x, p.y, p.z)

    if p.type == "speed":
        glColor3f(0.0, 1.0, 0.0)
        glutSolidCube(40)

    elif p.type == "range":
        glColor3f(1.0, 1.0, 0.0)
        glutSolidSphere(25, 12, 12)

    glPopMatrix()
