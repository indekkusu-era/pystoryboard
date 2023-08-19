from numpy import float16
from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Scalar:
    x: float

    def render(self, precision=float16):
        return f"{precision(self.x)}"

@dataclass(eq=True, frozen=True)
class Vector:
    x: float
    y: float

    def render(self, precision=float16):
        return f"{precision(self.x)},{precision(self.y)}"
    
@dataclass(eq=True, frozen=True)
class Color:
    r: int
    g: int
    b: int

    def render(self, precision=None):
        return f"{self.r},{self.g},{self.b}"

@dataclass(eq=True, frozen=True)
class Parameter:
    parameter: str

    def render(self, precision=None):
        return f"{self.parameter}"

__all__ = ['Scalar', 'Vector', 'Color', 'Parameter']    
