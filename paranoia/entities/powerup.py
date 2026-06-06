"""
entities/powerup.py
Powerup pickup entity.
"""

from paranoia.constants import GRID_LENGTH, MAP_SIZE


class Powerup:
    """A collectible powerup placed in the world."""

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        self.name  = name
        self.type  = name.split()[0]   # "speed" or "range"
        self.taken = False
        self.x = (pos[0] - MAP_SIZE // 2) * GRID_LENGTH
        self.y = (pos[1] - MAP_SIZE // 2) * GRID_LENGTH
        self.z = 30
