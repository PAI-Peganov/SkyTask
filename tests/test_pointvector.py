import unittest
import numpy as np
from src.point_vector import *


class TestPointVector(unittest.TestCase):

    def test_initialization(self):
        point = PointVector(1.0, 2.0, 3.0)

        self.assertEqual(point.x, 1.0)
        self.assertEqual(point.y, 2.0)
        self.assertEqual(point.z, 3.0)

    def test_np_vector_property(self):
        point = PointVector(1.0, 2.0, 3.0)

        expected_array = np.array([1.0, 2.0, 3.0])
        np.testing.assert_array_equal(point.np_vector, expected_array)

    def test_np_vector_type(self):
        point = PointVector(4.0, 5.0, 6.0)

        self.assertIsInstance(point.np_vector, np.ndarray)

    def test_np_vector_values(self):
        point = PointVector(-1.5, 2.5, -3.5)

        expected_array = np.array([-1.5, 2.5, -3.5])
        np.testing.assert_array_equal(point.np_vector, expected_array)


if __name__ == '__main__':
    unittest.main()
