from src.sky_and_stars_imports import *
import unittest
from unittest.mock import MagicMock


class TestBasicShape(unittest.TestCase):
    def setUp(self):
        self.shape = BasicShape("test_shape")

    def test_initialization(self):
        self.assertEqual(self.shape.name, "test_shape")
        self.assertEqual(self.shape.x, 0.0)
        self.assertEqual(self.shape.y, 0.0)
        self.assertEqual(self.shape.z, 0.0)
        self.assertIsNone(self.shape.child_shapes)
        self.assertEqual(self.shape.last_update, 0)

    def test_set_method(self):
        self.shape.set(x=1.5, y=2.5, z=3.5, upd=10)
        self.assertEqual(self.shape.x, 1.5)
        self.assertEqual(self.shape.y, 2.5)
        self.assertEqual(self.shape.z, 3.5)
        self.assertEqual(self.shape.last_update, 10)

    def test_get_edit_params(self):
        params, set_func = self.shape.get_edit_params()
        self.assertEqual(
            params, [("x", "X", float), ("y", "Y", float), ("z", "Z", float)]
        )
        self.assertEqual(set_func, self.shape.set)

    def test_add_children(self):
        children = ["child1", "child2"]
        self.shape.add_children(children)
        self.assertEqual(self.shape.child_shapes, children)


class TestPoint(unittest.TestCase):
    def setUp(self):
        self.point = PointVector("test_point", 1.0, 2.0, 3.0)

    def test_initialization(self):
        self.assertEqual(self.point.name, "test_point")
        self.assertEqual(self.point.x, 1.0)
        self.assertEqual(self.point.y, 2.0)
        self.assertEqual(self.point.z, 3.0)

    def test_np_vector_property(self):
        np.testing.assert_array_equal(
            self.point.np_vector, np.array([1.0, 2.0, 3.0])
        )


class TestLightPoint(unittest.TestCase):
    def setUp(self):
        self.light = LightPoint("test_light", "lightGL", 1.0, 2.0, 3.0)

    def test_initialization(self):
        self.assertEqual(self.light.name, "test_light")
        self.assertEqual(self.light.lightGL, "lightGL")
        self.assertEqual(self.light.x, 1.0)
        self.assertEqual(self.light.y, 2.0)
        self.assertEqual(self.light.z, 3.0)


class TestSegment(unittest.TestCase):
    def setUp(self):
        self.point_a = PointVector("point_a", 0.0, 0.0, 0.0)
        self.point_b = PointVector("point_b", 1.0, 1.0, 1.0)
        self.segment = Segment("test_segment", self.point_a, self.point_b)

    def test_initialization(self):
        self.assertEqual(self.segment.name, "test_segment")
        self.assertEqual(self.segment.point_a, self.point_a)
        self.assertEqual(self.segment.point_b, self.point_b)

    def test_update_coordinates(self):
        self.segment.set(x=1.0, y=2.0, z=3.0, upd=1)
        self.assertEqual(self.point_a.x, 1.0)
        self.assertEqual(self.point_a.y, 2.0)
        self.assertEqual(self.point_a.z, 3.0)
        self.assertEqual(self.point_b.x, 2.0)
        self.assertEqual(self.point_b.y, 3.0)
        self.assertEqual(self.point_b.z, 4.0)
        self.assertEqual(self.segment.x, 0.0)
        self.assertEqual(self.segment.y, 0.0)
        self.assertEqual(self.segment.z, 0.0)


class TestFigure2(unittest.TestCase):
    def setUp(self):
        self.points = [PointVector(f"point_{i}", i, i, i) for i in range(3)]
        self.figure = Figure2("test_figure", self.points)

    def test_initialization(self):
        self.assertEqual(self.figure.name, "test_figure")
        self.assertEqual(len(self.figure.points), 3)

    def test_update_coordinates(self):
        self.figure.set(x=1.0, y=2.0, z=3.0, upd=1)
        for i, point in enumerate(self.figure.points):
            self.assertEqual(point.x, i + 1.0)
            self.assertEqual(point.y, i + 2.0)
            self.assertEqual(point.z, i + 3.0)
            self.assertEqual(point.last_update, 1)
        self.assertEqual(self.figure.x, 0.0)
        self.assertEqual(self.figure.y, 0.0)
        self.assertEqual(self.figure.z, 0.0)


class TestPlane(unittest.TestCase):
    def setUp(self):
        self.point = PointVector("plane_point", 0.0, 0.0, 0.0)
        self.plane = Plane("test_plane", self.point)

    def test_initialization(self):
        self.assertEqual(self.plane.name, "test_plane")
        np.testing.assert_array_equal(
            self.plane.normal, np.array([0.0, 0.0, 0.0])
        )
        self.assertEqual(self.plane.point_a, self.point)
        self.assertEqual(self.plane.redraw, 0)
        self.assertEqual(self.plane.contur, [])

    def test_count_new_z(self):
        self.plane.normal = np.array([1.0, 1.0, 1.0])
        z = self.plane.count_new_z(1.0, 1.0)
        self.assertEqual(z, -2.0)

    def test_add_contur(self):
        segment = Segment("seg", PointVector("p1", 0, 0, 0), PointVector("p2", 1, 1, 1))
        contur = Contur2("contur", [segment])
        self.plane.add_contur(contur)
        self.assertEqual(len(self.plane.contur), 1)


class TestPlaneBy3Point(unittest.TestCase):
    def setUp(self):
        self.points = [PointVector(f"point_{i}", i, i, i) for i in range(3)]
        self.plane = PlaneBy3Point("test_plane", *self.points)

    def test_initialization(self):
        self.assertEqual(self.plane.name, "test_plane")
        self.assertEqual(self.plane.point_b, self.points[1])
        self.assertEqual(self.plane.point_c, self.points[2])

    def test_update_plane(self):
        self.plane.update_plane()
        expected_normal = np.cross(
            self.points[0].np_vector - self.points[1].np_vector,
            self.points[2].np_vector - self.points[1].np_vector
        )
        np.testing.assert_array_equal(self.plane.normal, expected_normal)

    def test_update_coordinates(self):
        self.plane.set(x=1.0, y=2.0, z=3.0, upd=1)
        for point in [
            self.plane.point_a,
            self.plane.point_b,
            self.plane.point_c
        ]:
            self.assertEqual(point.last_update, 1)
        self.assertEqual(self.plane.x, 0.0)
        self.assertEqual(self.plane.y, 0.0)
        self.assertEqual(self.plane.z, 0.0)


class TestPlaneByPointSegment(unittest.TestCase):
    def setUp(self):
        self.point = PointVector("point", 0, 0, 0)
        self.segment = Segment(
            "seg", PointVector("p1", 1, 1, 1), PointVector("p2", 2, 2, 2)
        )
        self.plane = PlaneByPointSegment(
            "test_plane", self.point, self.segment
        )

    def test_initialization(self):
        self.assertEqual(self.plane.name, "test_plane")
        self.assertEqual(self.plane.point_b, self.segment.point_a)
        self.assertEqual(self.plane.point_c, self.segment.point_b)


class TestPlaneByPlane(unittest.TestCase):
    def setUp(self):
        self.base_point = PointVector("base_point", 0, 0, 0)
        self.base_plane = Plane("base_plane", self.base_point)
        self.base_plane.normal = np.array([1, 1, 1])
        self.point = PointVector("point", 1, 1, 1)
        self.plane = PlaneByPlane("test_plane", self.point, self.base_plane)

    def test_initialization(self):
        self.assertEqual(self.plane.name, "test_plane")
        self.assertEqual(self.plane.base_plane, self.base_plane)

    def test_update_plane(self):
        self.plane.update_plane()
        np.testing.assert_array_equal(
            self.plane.normal, self.base_plane.normal
        )

    def test_update_coordinates(self):
        self.plane.set(x=1.0, y=2.0, z=3.0, upd=1)
        self.assertEqual(self.plane.point_a.last_update, 1)
        self.assertEqual(self.plane.x, 0.0)
        self.assertEqual(self.plane.y, 0.0)
        self.assertEqual(self.plane.z, 0.0)


class TestFigure3(unittest.TestCase):
    def setUp(self):
        points = [PointVector(f"point_{i}", i, i, i) for i in range(3)]
        faces = [Figure2(f"face_{i}", points) for i in range(3)]
        self.figure = Figure3("test_figure", faces)

    def test_initialization(self):
        self.assertEqual(self.figure.name, "test_figure")
        self.assertEqual(len(self.figure.faces), 3)
        self.assertEqual(len(self.figure.points), 3)

    def test_update_coordinates(self):
        self.figure.set(x=1.0, y=2.0, z=3.0, upd=1)
        for face in self.figure.faces:
            self.assertEqual(face.last_update, 1)
        self.assertEqual(self.figure.x, 0.0)
        self.assertEqual(self.figure.y, 0.0)
        self.assertEqual(self.figure.z, 0.0)

    def test_get_center(self):
        center = self.figure.get_center()
        np.testing.assert_array_almost_equal(
            center, np.array([1.0, 1.0, 1.0])
        )


if __name__ == '__main__':
    unittest.main()
