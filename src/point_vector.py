import numpy as np


class PointVector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @property
    def np_vector(self):
        return np.array([self.x, self.y, self.z])