"""
rendering/camera.py
Camera projection setup and the distance-based colour attenuation function.
"""

from __future__ import annotations
import math
from typing import TYPE_CHECKING

from OpenGL.GL  import *
from OpenGL.GLU import *

from paranoia.constants import FOV_Y, VIEW_CONE_ANGLE, sin_table, cos_table

if TYPE_CHECKING:
    from paranoia.entities.player import Player


def setup_camera(
    width: int,
    height: int,
    cam_mode: str,
    camera_pos: tuple[float, float, float],
    player: Player,
) -> None:
    """Configure the OpenGL projection and modelview matrices."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV_Y, width / height, 1.0, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if cam_mode == "tpv":
        cx, cy, cz = camera_pos
        gluLookAt(cx, cy, cz, 0, 0, 0, 0, 0, 1)

    elif cam_mode == "fpv":
        rad = math.radians(player.angle + 90)
        cx  = player.x
        cy  = player.y
        cz  = player.z + 200
        lx  = cx - math.cos(rad) * 200
        ly  = cy - math.sin(rad) * 200
        lz  = cz - 60
        gluLookAt(cx, cy, cz, lx, ly, lz, 0, 0, 1)


def color_func(
    x: float,
    y: float,
    r: float,
    g: float,
    b: float,
    player: Player,
) -> tuple[float, float, float]:
    """
    Return an attenuated (r, g, b) tuple based on distance and angle
    from the player's viewpoint, producing the torch-light effect.
    """
    vx   = x - player.x
    vy   = y - player.y
    dist = math.sqrt(vx * vx + vy * vy)

    if dist > player.view_range:
        bright = 0.05
    elif dist == 0:
        bright = 1.0
    else:
        vx /= dist
        vy /= dist

        dx   = sin_table[int(player.angle % 360)]
        dy   = -cos_table[int(player.angle % 360)]
        dlen = math.sqrt(dx * dx + dy * dy)
        dx  /= dlen
        dy  /= dlen

        dot       = vx * dx + vy * dy
        cos_cone  = cos_table[VIEW_CONE_ANGLE]
        angle_fac = max(0.0, (dot - cos_cone) / (1.0 - cos_cone))
        dist_fac  = max(1.0, 1.0 - (dist / player.view_range))

        bright = 0.05 + 0.95 * angle_fac * dist_fac

    return bright * r, bright * g, bright * b
