from dataclasses import dataclass
from ..constants import SB_LEFT, SB_RIGHT, SB_TOP, SB_BOTTOM

@dataclass
class PositionConfig:
    left: float = SB_LEFT
    right: float = SB_RIGHT
    top: float = SB_TOP
    bottom: float = SB_BOTTOM

    def convert_position(self, x, y):
        return (x - self.left) / (self.right - self.left) * (SB_RIGHT - SB_LEFT) + SB_LEFT, \
                    (y - self.top) / (self.bottom - self.top) * (SB_BOTTOM - SB_TOP) + SB_TOP
