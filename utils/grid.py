from dataclasses import dataclass

@dataclass
class Grid:
    top: float
    bottom: float
    left: float
    right: float
    division: tuple[int]

    @property
    def xrange(self):
        return self.right - self.left
    
    @property
    def yrange(self):
        return self.bottom - self.top

    def get_centre_position(self, pos: tuple[int]):
        xgrid, ygrid = ((pos[0] + 0.5) / self.division[0], (pos[1] + 0.5) / self.division[1])
        return xgrid * self.xrange + self.left, ygrid * self.yrange + self.top

def grid_from_center_point(center_point: tuple[float], radius: tuple[float], division: tuple[int]):
    cx, cy = center_point
    rx, ry = radius
    return Grid(
        top=cy - ry,
        bottom=cy + ry,
        left=cx - rx,
        right=cx + rx,
        division=division
    )

__all__ = ['Grid', 'grid_from_center_point']
