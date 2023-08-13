from enum import Enum

class Alignment(Enum):
    CENTRE = "Centre"
    TOP = "Top"
    BOTTOM = "Bottom"
    LEFT = "Left"
    RIGHT = "Right"
    BOTTOM_LEFT = "BottomLeft"
    BOTTOM_CENTRE = "BottomCentre"
    BOTTOM_RIGHT = "BottomRight"
    TOP_LEFT = "TopLeft"
    TOP_CENTRE = "TopCentre"
    TOP_RIGHT = "TopRight"

__all__ = ['Alignment']
