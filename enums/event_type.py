from enum import Enum

class EventType(Enum):
    SCALE = 'S'
    MOVE = 'M'
    FADE = 'F'
    ROTATE = 'R'
    COLOR = 'C'
    VECTORSCALE = 'V'
    MOVEX = 'MX'
    MOVEY = 'MY'
    PARAMETER = 'P'

class CompoundEventType(Enum):
    LOOP = 'L'
    TRIGGER = 'T'

__all__ = ['EventType', 'CompoundEventType']
