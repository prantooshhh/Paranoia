"""
input_handlers.py
GLUT input callback factories.

Each public function returns a closure pre-bound to the shared state
objects. Pass the result directly to the corresponding glutXxxFunc call.
This eliminates every `global` declaration that was previously inside
the callback bodies.
"""

from __future__ import annotations
import threading
from time import time
from typing import TYPE_CHECKING

from OpenGL.GLUT import *

from paranoia.constants import (
    GRID_LENGTH, RELOAD_TIME,
    CAM_HEIGHT_MIN, CAM_HEIGHT_MAX, CAM_HEIGHT_STEP, CAM_ANGLE_STEP,
)
from paranoia.map_data import GAME_MAP

if TYPE_CHECKING:
    from paranoia.entities.player   import Player
    from paranoia.entities.opponent import Opponent
    from paranoia.game_state        import GameState


# ── Keyboard ──────────────────────────────────────────────────────────────

def make_keyboard_down(gs: GameState, player: Player) -> callable:
    """Return a keyboardDown callback bound to gs and player."""

    def _cb(key: bytes, x: int, y: int) -> None:
        if gs.mode == "menu":
            if key == b"\r":
                gs.mode = "intro"

        elif gs.mode == "intro":
            if key == b"\r":
                gs.mode = "playing"

        if gs.mode != "over":
            if key == b"w": gs.controls.fw = True
            if key == b"s": gs.controls.bw = True
            if key == b"a": gs.controls.l  = True
            if key == b"d": gs.controls.r  = True

        if key == b"c":
            gs.cam = "tpv" if gs.cam == "fpv" else "fpv"

    return _cb


def make_keyboard_up(gs: GameState) -> callable:
    """Return a keyboardUp callback bound to gs."""

    def _cb(key: bytes, x: int, y: int) -> None:
        if gs.mode != "over":
            if key == b"w": gs.controls.fw = False
            if key == b"s": gs.controls.bw = False
            if key == b"a": gs.controls.l  = False
            if key == b"d": gs.controls.r  = False

    return _cb


# ── Special keys (arrow keys — TPV camera) ────────────────────────────────

def make_special_key(gs: GameState) -> callable:
    """Return a specialKey callback that orbits the TPV camera."""

    def _cb(key: int, x: int, y: int) -> None:
        cam = gs.camera
        if gs.cam == "tpv":
            if key == GLUT_KEY_UP:
                cam.height = min(cam.height + CAM_HEIGHT_STEP, CAM_HEIGHT_MAX)
            if key == GLUT_KEY_DOWN:
                cam.height = max(cam.height - CAM_HEIGHT_STEP, CAM_HEIGHT_MIN)
            if key == GLUT_KEY_LEFT:
                cam.angle -= CAM_ANGLE_STEP
            if key == GLUT_KEY_RIGHT:
                cam.angle += CAM_ANGLE_STEP

    return _cb


# ── Mouse ─────────────────────────────────────────────────────────────────

def make_mouse(
    gs: GameState,
    player: Player,
    opps: list[Opponent],
) -> callable:
    """Return a mouse callback that handles left-click shooting."""

    def _cb(button: int, state: int, x: int, y: int) -> None:
        if state != GLUT_DOWN:
            return
        if button != GLUT_LEFT_BUTTON:
            return
        if player.reloading:
            return

        gs.flash.gun_fired = True
        gs.flash.timer     = time()
        player.reloading   = True
        threading.Timer(RELOAD_TIME, player.reload).start()

        n = len(GAME_MAP)
        for opp in opps:
            if opp.x is None or opp.y is None:
                continue
            i = int(opp.x // GRID_LENGTH + n // 2)
            j = int(opp.y // GRID_LENGTH + n // 2)
            if player.active_blocks[i, j] == 2:
                opp.alive = False
                player.killed.append(opp.ip)

    return _cb
