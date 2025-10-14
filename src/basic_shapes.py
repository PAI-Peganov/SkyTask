from src.simple_3d_editor_imports import *


class BasicShape:
    def __init__(self, name: str):
        self.name = name

    def draw_shape(self):
        pass


class Point(BasicShape):
    def __init__(self, name: str, x: float, y: float, z: float):
        super().__init__(name)
        self.x = x
        self.y = y
        self.z = z

    def draw_shape(self):
        draw_point_param(self)

    @property
    def np_vector(self):
        return np.array([self.x, self.y, self.z])

        
class Star(BasicShape):
    def __init__(
            self, base_data: str, name: str, position: list[float],
            move: list[float], size: float, lightning: float, color: list[int],
            constellation: Constellation=None
    ):
        super().__init__(name)
        self.position = np.asarray(position)
        self.move = move
        self.size = size
        self.color = color
        self.lightning = lightning
        self.init_data = base_data
        self.constellation = constellation

    def draw_shape(self):
        draw_point_param(self.position, self.size, self.color)


class Segment(BasicShape):
    def __init__(self, name: str, a: Point, b: Point):
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
