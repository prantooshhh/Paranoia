"""
ui/screens.py
Full-screen 2D overlays: menu, scrolling intro, game-over, and winner.
"""

from dataclasses import dataclass, field
from time import time

from OpenGL.GL   import *
from OpenGL.GLUT import *

from paranoia.constants import INTRO_FPS
from paranoia.ui.text   import draw_text


# ── Intro state ─────────────────────────────────────────────────────────────

INTRO_LINES = [
    "You wake up surrounded by a deafening silence and darkness.....",
    "There's a torch and......a gun?",
    "Suddenly there are distant sounds of quiet rustling and footsteps! ",
    "",
    "The only way out is through.",
    "",
    "",
    "Press Enter to begin....",
]


@dataclass
class IntroState:
    """Tracks how many characters of the intro text have been revealed."""
    chars_shown: int = 0
    last_tick:   float = field(default_factory=time)

    def tick(self) -> None:
        """Advance the character counter at INTRO_FPS characters per second."""
        now = time()
        if now - self.last_tick >= 1.0 / INTRO_FPS:
            self.chars_shown += 1
            self.last_tick = now


# ── Draw functions ──────────────────────────────────────────────────────────

def draw_intro(intro: IntroState) -> None:
    char_count = 0
    for i, line in enumerate(INTRO_LINES):
        if intro.chars_shown > char_count:
            num_chars = min(len(line), intro.chars_shown - char_count)
            glColor3f(1, 0, 0) if i == len(INTRO_LINES) - 1 else glColor3f(1, 1, 1)
            draw_text(200, 500 - i * 50, line[:num_chars])
        char_count += len(line)


def draw_menu() -> None:
    glColor3f(1, 0, 0)
    draw_text(400, 500, "PARANOIA",                              GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(300, 450, "someone will have to end this nightmare first.....", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(200, 300, "Press ENTER to Start",                  GLUT_BITMAP_HELVETICA_12)
    draw_text(200, 270, "Use W-A-S-D to move around",            GLUT_BITMAP_HELVETICA_12)
    draw_text(200, 250, "Collect artifacts to use powerups",      GLUT_BITMAP_HELVETICA_12)
    draw_text(200, 230, "Left-click to fire",                    GLUT_BITMAP_HELVETICA_12)


def draw_game_over() -> None:
    glColor3f(1, 0, 0)
    draw_text(400, 400, "YOU ARE ELIMINATED")
    draw_text(400, 350, "Waiting for match to finish...")


def draw_winner() -> None:
    glColor3f(0, 1, 0)
    draw_text(400, 400, "Congratulations....")
