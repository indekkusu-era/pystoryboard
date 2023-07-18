import numpy as np
from numpy import sin, cos
from numpy.linalg import inv

class Camera:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), fov=np.pi/4):
        self._position = position
        self._rotation = rotation
        assert 0 < fov < np.pi/2
        self._fov = fov
    
    @property
    def position(self):
        return self._position
    
    @property
    def rotation(self):
        return self._rotation
    
    @position.setter
    def position(self, new_position):
        self._position = new_position
    
    @rotation.setter
    def rotation(self, new_rotation):
        self._rotation = new_rotation

    @staticmethod
    def rotation_matrix(theta, phi, psi):
        rx = np.array([[1,0,0], [0,cos(theta),-sin(theta)], [0,sin(theta),cos(theta)]])
        ry = np.array([[cos(phi),0,-sin(phi)], [0,1,0], [sin(phi),0,cos(phi)]])
        rz = np.array([[cos(psi),-sin(psi),0], [sin(psi),cos(psi),0], [0,0,1]])
        return rx @ ry @ rz
    
    def transform(self, object_position: tuple):
        x, y, z = object_position
        x_cam, y_cam, z_cam = self.position
        theta, phi, psi = self.rotation
        relative_pos = np.array((x - x_cam, y - y_cam, z - z_cam)).reshape(-1, 1)
        inv_size, x_2d, y_2d = (self.rotation_matrix(-theta, -phi, -psi) @ relative_pos).flatten()
        if inv_size <= 0:
            return (0, 0), 0

        size = 1 / (inv_size * np.tan(self.fov))
        return (x_2d * size, y_2d * size), size
