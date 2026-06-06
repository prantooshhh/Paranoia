"""
__main__.py
Entry point for Paranoia.  Run with:  python -m paranoia

Responsibilities:
  1. Prompt for server IP.
  2. Connect to server and block until all players are ready.
  3. Build entity objects from the server's start payload.
  4. Initialise OpenGL / GLUT.
  5. Register callbacks and start the main loop.
"""

from OpenGL.GL   import *
from OpenGL.GLUT import *

from paranoia.constants       import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, TESTING
from paranoia.network         import NetworkClient, DummyNetworkClient
from paranoia.game_state      import GameState
from paranoia.ui.screens      import IntroState

from paranoia.entities.player   import Player
from paranoia.entities.opponent import Opponent
from paranoia.entities.powerup  import Powerup

from paranoia.input_handlers import (
    make_keyboard_down,
    make_keyboard_up,
    make_special_key,
    make_mouse,
)
from paranoia.game_loop import make_idle, make_show_screen


# Powerup name mapping: keys must match server's spawn-index order
_POWERUP_NAMES = ["speed 1", "speed 2", "speed 3", "range 1", "range 2", "range 3"]


def main() -> None:
    # ── 1. Network handshake ─────────────────────────────────────────────
    if TESTING:
        net = DummyNetworkClient()
    else:
        server_ip = input("Enter server IP: ")
        net       = NetworkClient(server_ip)

    net.connect()

    # ── 2. Wait for all players ──────────────────────────────────────────
    if not TESTING:
        print("Waiting for other players...")
    payload = net.wait_for_start()

    # ── 3. Build entities ────────────────────────────────────────────────
    player = Player(ip=net.local_ip, start_pos=payload.player_start)

    opps = [Opponent(ip) for ip in payload.players]

    powerup_map = {
        name: payload.powerup_spawns[i]
        for i, name in enumerate(_POWERUP_NAMES)
    }
    powerups = [Powerup(name, pos) for name, pos in powerup_map.items()]

    # ── 4. Game state ────────────────────────────────────────────────────
    gs          = GameState()
    gs.intro    = IntroState()
    gs.local_ip = net.local_ip

    # ── 5. OpenGL / GLUT init ────────────────────────────────────────────
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(WINDOW_TITLE)

    glEnable(GL_DEPTH_TEST)

    # ── 6. Register callbacks ────────────────────────────────────────────
    glutDisplayFunc (make_show_screen(gs, player, opps, powerups, WINDOW_WIDTH, WINDOW_HEIGHT))
    glutIdleFunc    (make_idle(gs, player, opps, powerups, net))
    glutKeyboardFunc(make_keyboard_down(gs, player))
    glutKeyboardUpFunc(make_keyboard_up(gs))
    glutSpecialFunc (make_special_key(gs))
    glutMouseFunc   (make_mouse(gs, player, opps))

    # ── 7. Enter main loop ───────────────────────────────────────────────
    glutMainLoop()


if __name__ == "__main__":
    main()
