import numpy as np
from .events import Event, Move, Scale
from three_dimensions.camera_3d import Camera

def sample(z0, z1, eps=1e-2):
    """Sample the z coordinates for approximating size linearly"""
    z_sample = z0
    t = 0
    eps = min(1 / max(z0, z1), eps) 
    if z0 > z1:
        s0 = 1 / z0
        s1_bound = eps + s0 + 2 * np.sqrt(s0 * eps)
        z1_bound = 1 / s1_bound
        while z_sample > z1:
            t = (z_sample - z0) / (z1 - z0)
            yield 1 / z_sample, t
            z_sample = z1_bound
            s0 = 1 / z_sample
            s1_bound = eps + s0 + 2 * np.sqrt(s0 * eps)
            z1_bound = 1 / s1_bound
    elif z0 < z1:
        s0 = 1 / z0
        s1_bound = eps + s0 - 2 * np.sqrt(s0 * eps)
        z1_bound = 1 / s1_bound
        while z_sample < z1:
            t = (z_sample - z0) / (z1 - z0)
            yield 1 / z_sample, t
            z_sample = z1_bound
            s0 = 1 / z_sample
            s1_bound = eps + s0 - 2 * np.sqrt(s0 * eps)
            z1_bound = 1 / s1_bound
    else:
        yield 1 / z0, 0
        yield 1 / z1, 1
    yield 1 / z1, 1

class ThreeDimensionsMove(Event):
    def __init__(self, easing: int, start_time: int, end_time: int, start_3d_position: tuple[int], end_3d_position: tuple[int]) -> None:
        self.easing = easing
        self.start_time = start_time
        self.end_time = end_time
        self.start_3d_position = start_3d_position
        self.end_3d_position = end_3d_position
    
    def _transform(self, camera: Camera):
        (x0, y0), size0 = camera.transform(self.start_3d_position)
        (x1, y1), size1 = camera.transform(self.end_3d_position)
        move_event = Move(self.easing, self.start_time, self.end_time, (x0, y0), (x1, y1))
        scale_event = Scale(self.easing, self.start_time, self.end_time, size0, size1)
        return move_event, scale_event
    
    def render(self, camera: Camera):
        """To be fixed"""
        move_event, scale_event = self._transform(camera)
        return [move_event.render(), scale_event.render()] 
        
