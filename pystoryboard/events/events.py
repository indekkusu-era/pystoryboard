from numpy import float16
from typing import Any
from .event_classes import TimeRange, make_event_value, Scalar, Vector, Color as _Color, Parameter as _Parameter
from ..enums import EventType, Easing, Parameters

class Event:
    def __init__(self, event_type: EventType, time_range: TimeRange, event_maker: Any, easing: Easing) -> None:
        self.event_type = event_type
        self.easing = easing
        self.time_range = time_range
        self.event_maker = event_maker

    def offset(self, offset: int):
        self.time_range.offset(offset)
        return self

    def __repr__(self):
        return f"""{self.event_type.name}({self.time_range.__repr__()} | value: {self.event_maker.__repr__()} | easing: {self.easing.name})"""
    
    def render(self, precision=float16):
        return f"{self.event_type.value},{self.easing.value},{self.time_range.render()},{self.event_maker.render(precision)}"

class ScalarEvent(Event):
    def __init__(self, event_type: EventType, start_time: int, end_time: int, start_scalar: float, end_scalar: float, easing: Easing):
        super().__init__(event_type, TimeRange(start_time, end_time), make_event_value(Scalar)(Scalar(start_scalar), Scalar(end_scalar)), easing)

class VectorEvent(Event):
    def __init__(self, event_type: EventType, start_time: int, end_time: int, start_vector: Vector, end_vector: Vector, easing: Easing):
        super().__init__(event_type, TimeRange(start_time, end_time), make_event_value(Vector)(start_vector, end_vector), easing)

class ColorEvent(Event):
    def __init__(self, event_type: EventType, start_time: int, end_time: int, start_color: _Color, end_color: _Color, easing: Easing):
        super().__init__(event_type, TimeRange(start_time, end_time), make_event_value(Color)(start_color, end_color), easing)

class Scale(ScalarEvent):
    def __init__(self, start_time: int, end_time: int, start_scale: float, end_scale: float, easing=Easing.LINEAR) -> None:
        super().__init__(EventType.SCALE, start_time, end_time, start_scale, end_scale, easing)

class Move(VectorEvent):
    def __init__(self, start_time: int, end_time: int, start_position: Vector, end_position: Vector, easing=Easing.LINEAR) -> None:
        super().__init__(EventType.MOVE, start_time, end_time, start_position, end_position, easing)

class Fade(ScalarEvent):
    def __init__(self, start_time: int, end_time: int, start_opacity: float, end_opacity: float, easing=Easing.LINEAR) -> None:
        super().__init__(EventType.FADE, start_time, end_time, start_opacity, end_opacity, easing)

class Rotate(ScalarEvent):
    def __init__(self, start_time: int, end_time: int, start_angle: float, end_angle: float, easing=Easing.LINEAR) -> None:
        super().__init__(EventType.ROTATE, start_time, end_time, start_angle, end_angle, easing)

class Color(ColorEvent):
    def __init__(self, start_time: int, end_time: int, start_color: _Color, end_color: _Color, easing=Easing.LINEAR):
        super().__init__(EventType.COLOR, start_time, end_time, start_color, end_color, easing)

class VectorScale(VectorEvent):
    def __init__(self, start_time: int, end_time: int, start_vector: Vector, end_vector: Vector, easing=Easing.LINEAR) -> None:
        super().__init__(EventType.VECTORSCALE, start_time, end_time, start_vector, end_vector, easing)

class MoveX(ScalarEvent):
    def __init__(self, start_time: int, end_time: int, start_x: float, end_x: float, easing=Easing.LINEAR) -> None:
        super().__init__(EventType.MOVEX, start_time, end_time, start_x, end_x, easing)

class MoveY(ScalarEvent):
    def __init__(self, start_time: int, end_time: int, start_y: float, end_y: float, easing=Easing.LINEAR) -> None:
        super().__init__(EventType.MOVEY, start_time, end_time, start_y, end_y, easing)

class Parameter(Event):
    def __init__(self, start_time: int, end_time: int, parameter: Parameters, easing=Easing.LINEAR):
        super().__init__(EventType.PARAMETER, TimeRange(start_time, end_time), make_event_value(_Parameter)(parameter, parameter), easing)

__all__ = ['Scale', 'Move', 'Fade', 'Rotate', 'Color', 'VectorScale', 'MoveX', 'MoveY', 'Parameter', 'Event']
