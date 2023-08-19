from enum import Enum

class Alignment(Enum):
    CENTRE = "Centre"
    CENTRE_LEFT = "CentreLeft"
    CENTRE_RIGHT = "CentreRight"
    BOTTOM_LEFT = "BottomLeft"
    BOTTOM_CENTRE = "BottomCentre"
    BOTTOM_RIGHT = "BottomRight"
    TOP_LEFT = "TopLeft"
    TOP_CENTRE = "TopCentre"
    TOP_RIGHT = "TopRight"

__all__ = ['Alignment']
