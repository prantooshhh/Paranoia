"""
ui/text.py
Utility for drawing bitmap text into the current OpenGL context
using a temporary orthographic projection.
"""

from OpenGL.GL   import *
from OpenGL.GLU  import *
from OpenGL.GLUT import *


def draw_text(
    x: float,
    y: float,
    text: str,
    font=GLUT_BITMAP_TIMES_ROMAN_24,  # type: ignore[assignment]
) -> None:
    """
    Render a string at window-space coordinates (x, y).

    The function temporarily switches to a 1000×800 orthographic
    projection, draws the text, and restores the previous matrices.
    """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
