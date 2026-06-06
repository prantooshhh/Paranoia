"""
game_loop.py
Core GLUT loop callbacks: idle() and show_screen().

idle()        — physics, powerup collection, network, and intro ticker.
show_screen() — top-level render dispatcher: clears buffers and delegates
                to the correct subsystem based on game mode.

Both functions are exposed as factories so that the shared state objects
can be injected by __main__.py without using module-level globals.
"""

from __future__ import annotations
from time import time
from typing import TYPE_CHECKING

from OpenGL.GL   import *
from OpenGL.GLUT import *

from paranoia.constants  import GRID_LENGTH, GUN_FLASH_DURATION, TESTING
from paranoia.map_data   import GAME_MAP

from paranoia.rendering.camera            import setup_camera
from paranoia.rendering.world             import draw_map
from paranoia.rendering.characters        import draw_player, draw_creature
from paranoia.rendering.powerups_renderer import draw_powerup

from paranoia.ui.minimap  import draw_minimap
from paranoia.ui.screens  import draw_intro, draw_menu, draw_game_over, draw_winner

if TYPE_CHECKING:
    from paranoia.entities.player   import Player
    from paranoia.entities.opponent import Opponent
    from paranoia.entities.powerup  import Powerup
    from paranoia.game_state        import GameState
    from paranoia.network           import NetworkClient


# ── Powerup proximity check ───────────────────────────────────────────────

def _powerup_hitbox(player: Player, collectible: Powerup) -> bool:
    """Return True when the player is close enough to collect the powerup."""
    player_size     = 20
    collectible_size = 15
    return (
        abs(player.x - collectible.x) <= player_size + collectible_size
        and abs(player.y - collectible.y) <= player_size + collectible_size
    )


# ── Delta-time tracker ────────────────────────────────────────────────────

class _DeltaTimer:
    def __init__(self) -> None:
        self._last = time()

    def tick(self) -> float:
        now        = time()
        dt         = now - self._last
        self._last = now
        return dt


# ── Factory: idle callback ────────────────────────────────────────────────

def make_idle(
    gs: GameState,
    player: Player,
    opps: list[Opponent],
    powerups: list[Powerup],
    net: NetworkClient,
) -> callable:
    """Return an idle() callback pre-bound to the game's shared state."""

    timer = _DeltaTimer()

    def _idle() -> None:
        dt = timer.tick()

        # Network update (rate-limited)
        if net.should_send():
            net.send_recv_update(player, opps, powerups)

        if gs.mode == "playing":
            # Movement controls
            if gs.controls.fw: player.go_forward(dt)
            if gs.controls.bw: player.go_backward(dt)
            if gs.controls.l:  player.rotate_left(dt)
            if gs.controls.r:  player.rotate_right(dt)

            # Powerup collection
            for p in powerups:
                if p.taken:
                    continue
                if _powerup_hitbox(player, p):
                    player.powerups_name.append(p.name)
                    player.collect_powerup(p.type)
                    p.taken = True

            # Clear muzzle flash after its duration
            if gs.flash.gun_fired and (time() - gs.flash.timer) > GUN_FLASH_DURATION:
                gs.flash.gun_fired = False

        elif gs.mode == "intro":
            gs.intro.tick()

        glutPostRedisplay()

    return _idle


# ── Factory: show_screen callback ─────────────────────────────────────────

def make_show_screen(
    gs: GameState,
    player: Player,
    opps: list[Opponent],
    powerups: list[Powerup],
    width: int,
    height: int,
) -> callable:
    """Return a showScreen() callback pre-bound to the game's shared state."""

    def _show_screen() -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, width, height)

        # Eliminate player as soon as they die
        if not player.alive:
            gs.mode = "over"

        if gs.mode == "intro":
            draw_intro(gs.intro)

        elif gs.mode == "menu":
            draw_menu()

        elif gs.mode == "playing":
            setup_camera(width, height, gs.cam, gs.camera.position, player)
            draw_player(player, game_over=False, gun_fired=gs.flash.gun_fired)
            draw_map(player)

            for p in powerups:
                if not p.taken:
                    draw_powerup(p)

            all_alive_opponents = False
            n = len(GAME_MAP)
            for opp in opps:
                if opp.x is not None and opp.y is not None:
                    i = int(opp.x // GRID_LENGTH + n // 2)
                    j = int(opp.y // GRID_LENGTH + n // 2)
                    if player.active_blocks[i, j] == 2:
                        draw_creature(opp.x, opp.y, 0, opp.alive, player)
                if opp.alive and opp.ip != gs.local_ip:
                    all_alive_opponents = True

            if not all_alive_opponents and not TESTING:
                gs.mode = "won"

            draw_minimap(width, height, player, powerups)

        elif gs.mode == "over":
            draw_game_over()

        elif gs.mode == "won":
            draw_winner()

        glutSwapBuffers()

    return _show_screen
