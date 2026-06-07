"""
game_state.py
Lightweight containers for shared mutable state.
Passing these objects into callbacks avoids the global keyword.
"""

import math
from dataclasses import dataclass, field

from paranoia.constants import (
    CAM_ANGLE_DEFAULT, CAM_RADIUS_DEFAULT, CAM_HEIGHT_DEFAULT,
    GUN_FLASH_DURATION,
)


@dataclass
class Controls:
    """Keyboard movement state — True while a key is held."""
    fw: bool = False
    bw: bool = False
    l:  bool = False
    r:  bool = False


@dataclass
class CameraState:
    """Third-person camera orbit parameters."""
    angle:  float = CAM_ANGLE_DEFAULT
    radius: float = CAM_RADIUS_DEFAULT
    height: float = CAM_HEIGHT_DEFAULT

    @property
    def position(self) -> tuple[float, float, float]:
        x = self.radius * math.cos(self.angle)
        y = self.radius * math.sin(self.angle)
        return (x, y, self.height)


@dataclass
class FlashState:
    """Muzzle-flash display state."""
    gun_fired:      bool  = False
    timer:          float = 0.0
    flash_duration: float = GUN_FLASH_DURATION


@dataclass
class GameState:
    """Top-level game mode and camera-mode selector."""
    mode: str = "menu"   # "menu" | "intro" | "playing" | "over" | "won"
    cam:  str = "fpv"    # "fpv"  | "tpv"

    controls: Controls    = field(default_factory=Controls)
    camera:   CameraState = field(default_factory=CameraState)
    flash:    FlashState  = field(default_factory=FlashState)