from src.simple_3d_editor_imports import *


class BasicShape:
    def __init__(self, name: str):
        self.name = name
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.child_shapes = None
        self.last_update = 0

    def set(self, **kwargs):
        if self.last_update == kwargs["upd"]:
            return
        for tag, value in kwargs.items():
            if tag == "upd":
                self.__setattr__(
                    "last_update",
                    type(self.__getattribute__("last_update"))(value)
                )
                continue
            if not isinstance(value, type(self.__getattribute__(tag))):
                print(type(value) + "некорректен")
            self.__setattr__(tag, type(self.__getattribute__(tag))(value))
        self.update_coordinates()

    def update_coordinates(self):
        pass

    def get_edit_params(self):
        return [
            ("x", "X", float),
            ("y", "Y", float),
            ("z", "Z", float)
        ], self.set

    def draw_shape(self):
        pass

    def add_children(self, list_children):
        self.child_shapes = list(list_children)


class Point(BasicShape):
    def __init__(self, name: str, x: float, y: float, z: float):
        super().__init__(name)
        self.x = x
        self.y = y
        self.z = z

    def draw_shape(self):
        draw_point(self)

    @property
    def np_vector(self):
        return np.array([self.x, self.y, self.z])


class LightPoint(Point):
    def __init__(self, name: str, lightGL, x: float, y: float, z: float):
        super().__init__(name, x, y, z)
        self.lightGL = lightGL

    def draw_shape(self):
        draw_light(self)


class Segment(BasicShape):
    def __init__(self, name: str, a: Point, b: Point):
        super().__init__(name)
        self.point_a = a
        self.point_b = b

    def draw_shape(self):
        draw_segment(self)

    def update_coordinates(self):
        if self.point_a.last_update != self.last_update:
            self.point_a.last_update = self.last_update
            self.point_a.x += self.x
            self.point_a.y += self.y
            self.point_a.z += self.z
        if self.point_b.last_update != self.last_update:
            self.point_b.last_update = self.last_update
            self.point_b.x += self.x
            self.point_b.y += self.y
            self.point_b.z += self.z
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


class Figure2(BasicShape):
    def __init__(self, name: str, points: list[Point]):
        super().__init__(name)
        self.points = list(points)

    def draw_shape(self):
        draw_figure2(self)

    def update_coordinates(self):
        for point in self.points:
            if point.last_update == self.last_update:
                continue
            point.x += self.x
            point.y += self.y
            point.z += self.z
            point.last_update = self.last_update
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


class Contur2(BasicShape):
    def __init__(self, name: str, segments: list[Segment]):
        super().__init__(name)
        self.segments = list(segments)


class Plane(BasicShape):
    def __init__(self, name: str, point: Point):
        super().__init__(name)
        self.normal = np.array([0.0, 0.0, 0.0], dtype=float)
        self.point_a = point
        self.redraw = 0
        self.contur = []

    def update_plane(self):
        pass

    def update_contur(self):
        for contur in self.contur:
            for i in range(len(contur.segments)):
                new_z = self.count_new_z(
                    contur.segments[i].point_a.x,
                    contur.segments[i].point_a.y
                )
                contur.segments[i].point_a.z = new_z
                contur.segments[i - 1].point_b.z = new_z

    def add_contur(self, contur: Contur2):
        self.contur.append(contur)
        self.update_contur()

    def count_new_z(self, x, y):
        return sum(
            [
                (self.point_a.x - x) * self.normal[0],
                (self.point_a.y - y) * self.normal[1],
                self.point_a.z * self.normal[2]
            ]
        ) / self.normal[2]

    def draw_shape(self):
        self.redraw -= 1
        if self.redraw < 0:
            self.redraw = np.random.randint(5, 15)
            self.update_plane()
        draw_plane(self)


class PlaneBy3Point(Plane):
    def __init__(
            self, name: str, point_a: Point, point_b: Point, point_c: Point
    ):
        super().__init__(name, point_a)
        self.point_b = point_b
        self.point_c = point_c
        self.update_plane()

    def update_plane(self):
        self.normal = np.cross(
            self.point_a.np_vector - self.point_b.np_vector,
            self.point_c.np_vector - self.point_b.np_vector
        )
        self.update_contur()

    def update_coordinates(self):
        for point in [self.point_a, self.point_b, self.point_c]:
            if point.last_update != self.last_update:
                point.x += self.x
                point.y += self.y
                point.z += self.z
                point.last_update = self.last_update
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


class PlaneByPointSegment(PlaneBy3Point):
    def __init__(self, name: str, point: Point, segment: Segment):
        super().__init__(name, point, segment.point_a, segment.point_b)
        self.update_plane()


class PlaneByPlane(Plane):
    def __init__(self, name: str, point: Point, plane: Plane):
        super().__init__(name, point)
        self.base_plane = plane
        self.update_plane()

    def update_plane(self):
        self.normal = np.array(self.base_plane.normal)
        self.update_contur()

    def update_coordinates(self):
        if self.point_a.last_update != self.last_update:
            self.point_a.x += self.x
            self.point_a.y += self.y
            self.point_a.z += self.z
            self.point_a.last_update = self.last_update
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


class Figure3(BasicShape):
    def __init__(self, name: str, faces: list[Figure2]):
        super().__init__(name)
        self.faces = list(faces)
        self.points = set()
        self.init_points()

    def init_points(self):
        for face in self.faces:
            for point in face.points:
                self.points.add(point)

    def update_coordinates(self):
        for face in self.faces:
            if face.last_update == self.last_update:
                continue
            face.set(x=self.x, y=self.y, z=self.z, upd=self.last_update)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def draw_shape(self):
        draw_figure3(self)

    def get_center(self):
        return np.mean([p.np_vector for p in self.points], axis=0)
