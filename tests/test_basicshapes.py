import unittest
from unittest.mock import patch
from src.base_entities import *
from src.shape_opengl_drawers import *


class TestStar(unittest.TestCase):

    def test_star_initialization(self):
        star = Star(
            name="Alpha",
            hd_number="HD 12345",
            longitude=180.0,
            latitude=45.0,
            init_year=2000,
            move_longitude_seconds=0.1,
            move_latitude_seconds=0.1,
            magnitude=5.0,
            spectral_class="G",
            reference={"key": "value"},
            constellation_name="Orion"
        )

        self.assertEqual(star.name, "Alpha")
        self.assertEqual(star.hd_number, "HD 12345")
        self.assertEqual(star.longitude, 180.0)
        self.assertEqual(star.latitude, 45.0)
        self.assertEqual(star.magnitude, 5.0)

    @patch('src.shape_opengl_drawers.draw_point_param')
    def test_star_draw_shape(self, mock_draw_point_param):
        star = Star(
            name="Beta",
            hd_number="54321",
            longitude=120.0,
            latitude=30.0,
            init_year=2000,
            move_longitude_seconds=0.1,
            move_latitude_seconds=0.1,
            magnitude=4.0,
            spectral_class="A",
            reference={"key": "value"},
            constellation_name="Andromeda"
        )

        star.draw_shape()

        mock_draw_point_param.assert_called_once()

    def test_star_position_update(self):
        star = Star(
            name="Gamma",
            hd_number="HD 67890",
            longitude=90.0,
            latitude=-45.0,
            init_year=2000,
            move_longitude_seconds=0.2,
            move_latitude_seconds=0.2,
            magnitude=3.0,
            spectral_class="M",
            reference={"key": "value"},
            constellation_name="Cassiopeia"
        )

        star.set_time_span(2020)

        pos = star.get_position_numpy()
        self.assertIsNotNone(pos)


if __name__ == '__main__':
    unittest.main()
