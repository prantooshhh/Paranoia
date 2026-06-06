"""
map_data.py
Builds and exposes the static game map.

Map cell values:
    0 — black / out-of-bounds void
    1 — wall
    2 — free walkable space
"""

import numpy as np


def make_map() -> np.ndarray:
    """Return a (102 x 102) int array describing the level layout."""
    grid = np.array([[2 for _ in range(102)] for _ in range(102)])

    # Outer boundary walls
    grid[0, :]   = 1
    grid[-1, :]  = 1
    grid[:, 0]   = 1
    grid[:, -1]  = 1

    # Section 1
    grid[20, :11]    = 1
    grid[20:81, 10]  = 1
    grid[80, 1:10]   = 1
    grid[30, 11:21]  = 1
    grid[21:80, 0:10] = 0

    # Section 2
    grid[1:11, 10]    = 1
    grid[10, 10:55]   = 1
    grid[10:25, 54]   = 1
    grid[24, 54:66]   = 1
    grid[10:36, 65]   = 1
    grid[10, 65:91]   = 1
    grid[1:11, 90]    = 1
    grid[11:31, 28]   = 1
    grid[0:10, 11:90] = 0
    grid[10:24, 55:65] = 0

    # Section 3
    grid[91:101, 10]  = 1
    grid[91, 10:53]   = 1
    grid[77:91, 52]   = 1
    grid[77, 52:61]   = 1
    grid[77:92, 60]   = 1
    grid[91, 60:91]   = 1
    grid[91:101, 90]  = 1
    grid[71:91, 40]   = 1
    grid[92:102, 11:90] = 0
    grid[78:92, 53:60]  = 0

    # Section 4
    grid[20, 90:101]  = 1
    grid[20:81, 90]   = 1
    grid[80, 90:101]  = 1
    grid[35, 75:90]   = 1
    grid[21:80, 91:102] = 0

    # Section 5
    grid[40:76, 28]   = 1
    grid[75, 20:29]   = 1
    grid[57:76, 20]   = 1
    grid[57, 20:28]   = 1
    grid[58:75, 21:28] = 0

    # Section 6
    grid[32:58, 40]   = 1
    grid[57, 40:61]   = 1
    grid[51:58, 60]   = 1
    grid[50, 40:74]   = 1
    grid[50:77, 73]   = 1
    grid[51:57, 41:60] = 0

    # Section 7
    grid[64, 40:61]   = 1

    return grid


# Single shared instance — import GAME_MAP everywhere instead of rebuilding.
GAME_MAP: np.ndarray = make_map()
