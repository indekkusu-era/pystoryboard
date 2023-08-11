from enum import Enum

class Layers(Enum):
    BACKGROUND = "Background"
    FAIL = "Fail"
    PASS = "Pass"
    FOREGROUND = "Foreground"
    OVERLAY = "Overlay"

__all__ = ['Layers']
