"""
constants.py
All named constants for Paranoia. Import from here instead of using magic numbers.
"""

import math

# ── Development ─────────────────────────────────────────────────────────────
# Set TESTING = True to run solo without a server (single-player debug mode).
# Set TESTING = False for normal LAN multiplayer.
TESTING = True

# ── Window ─────────────────────────────────────────────────────────────────
WINDOW_WIDTH  = 1200
WINDOW_HEIGHT = 690
WINDOW_TITLE  = b"Paranoia"

# ── World / grid ────────────────────────────────────────────────────────────
GRID_LENGTH   = 50
PLAYER_RADIUS = 20
MAP_SIZE      = 102   # side length of the square map array

# ── Camera ──────────────────────────────────────────────────────────────────
CAM_ANGLE_DEFAULT  = math.pi / 2
CAM_RADIUS_DEFAULT = 800
CAM_HEIGHT_DEFAULT = 800
CAM_HEIGHT_MIN     = 400
CAM_HEIGHT_MAX     = 1320
CAM_HEIGHT_STEP    = 10
CAM_ANGLE_STEP     = 0.01
FOV_Y              = 90

# ── Player defaults ─────────────────────────────────────────────────────────
BASE_SPEED             = 140
BASE_VIEW_RANGE        = 450
BASE_VIEW_RANGE_ACTIVE = 5   # cone range in grid cells
ROTATION_SPEED         = 50  # degrees per second
VIEW_CONE_ANGLE        = 45  # degrees
AROUND_RENDER_RADIUS   = 17  # always-rendered square half-size (grid cells)

# Powerup limits
SPEED_BOOST       = 40
SPEED_MAX         = 200
RANGE_BOOST       = 650
RANGE_ACTIVE_BOOST = 7

# ── Timing ──────────────────────────────────────────────────────────────────
SEND_INTERVAL     = 0.05   # seconds between network updates
RELOAD_TIME       = 2.0    # seconds before player can fire again
GUN_FLASH_DURATION = 0.1   # seconds the muzzle flash stays visible
INTRO_FPS         = 20     # characters revealed per second

# ── Network ─────────────────────────────────────────────────────────────────
ENCODING          = "utf-8"
SERVER_PORT       = 8000
CONNECT_MSG       = "connect"
DISCONNECT_MSG    = "disconnect"
CHECK_START_MSG   = "s"
NOT_START_MSG     = "wait"
RECV_BUFFER       = 65535

# ── Precomputed trig tables (avoids repeated sin/cos in hot paths) ───────────
sin_table = [math.sin(math.radians(a)) for a in range(360)]
cos_table = [math.cos(math.radians(a)) for a in range(360)]
