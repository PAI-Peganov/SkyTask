from src.shape_opengl_drawers import *
from src.point_vector import PointVector


class BasicShape:
    def __init__(self, name: str):
        self.name = name

    def draw_shape(self):
        pass

        
class Star(BasicShape):
    def __init__(
            self, name: str,
            position: PointVector, move: list[float],
            size: float, lightning: float, color: list[int],
            constellation_name: str =None
    ):
        super().__init__(name)
        self.position = position
        self.move = move
        self.size = size
        self.color = color
        self.lightning = lightning
        self.constellation_name = constellation_name

    def draw_shape(self):
        draw_point_param(self.position, self.size, self.color)


class Segment(BasicShape):
    def __init__(self, name: str, a: PointVector, b: PointVector):
        super().__init__(name)
        self.point_a = a
        self.point_b = b

    def draw_shape(self):
        draw_segment(self)


class Constellation(BasicShape):
    def __init__(self, name: str, stars: list[Star], segments: list[Segment]):
        super().__init__(name)
        self.stars = list(stars)
        self.segments = list(segments)

    def draw_shape(self):
        draw_constellation(self)
