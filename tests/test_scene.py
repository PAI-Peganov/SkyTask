import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import numpy as np
from src.base_entities import *
from src.scene_base import *


class TestScene(unittest.TestCase):

    @patch('src.star_parser.parse_star_data_from_zip')
    def test_add_stars_from_zip(self, mock_parse_star_data_from_zip):
        mock_parse_star_data_from_zip.return_value = [
            {
                "name": "Alpha",
                "id": "HD12345",
                "galactic_lon": 10.0,
                "galactic_lat": 20.0,
                "move_longitude": 0.1,
                "move_latitude": 0.1,
                "magnitude": 4.5,
                "spectral_class": "G",
            }
        ]

        scene = Scene()
        mock_path = Path("test_stars.zip")
        scene._add_stars_from_zip(mock_path)

        self.assertEqual(len(scene._stars), 1)
        self.assertEqual(scene._stars[0].name, "Alpha")
        self.assertEqual(scene._stars[0].hd_number, "HD12345")

    @patch('src.star_parser.parse_constellation_data_from_json')
    def test_add_constellations_from_json(self, mock_parse_constellation_data_from_json):
        mock_parse_constellation_data_from_json.return_value = [
            {"name": "Orion", "lines": [["HD12345", "HD67890"]]}
        ]

        scene = Scene()
        mock_path_stars = Path("test_stars.zip")
        mock_path_constellations = Path("test_constellations.json")
        scene._add_stars_from_zip(mock_path_stars)
        scene._add_constellations_from_json(mock_path_constellations)

        self.assertEqual(len(scene._constellations), 1)
        self.assertEqual(scene._constellations[0].name, "Orion")
        self.assertEqual(len(scene._constellations[0].star_polylines), 1)

    def test_set_magnitude_filter_range(self):
        scene = Scene()

        scene.set_magnitude_filter_range(4, 6)
        self.assertEqual(scene._magnitude_min, 4)
        self.assertEqual(scene._magnitude_max, 6)

        star = Star(
            name="Alpha", hd_number="HD12345", longitude=0, latitude=0,
            init_year=2000, move_longitude_seconds=0.1, move_latitude_seconds=0.1,
            magnitude=5, spectral_class="G", reference={}, constellation_name=""
        )
        scene._stars.append(star)
        scene._update_filtered_list_stars()
        self.assertEqual(len(scene._filtered_stars), 1)

    def test_set_position_on_earth(self):
        scene = Scene()
        scene.set_position_on_earth(latitude=45.0, longitude=90.0)

        expected_position = PointVector(
            math.cos(90.0 * math.pi / 180 + math.pi) *
            math.cos(-45.0 * math.pi / 180) * 55,
            math.sin(90.0 * math.pi / 180 + math.pi) *
            math.cos(-45.0 * math.pi / 180) * 55,
            math.sin(-45.0 * math.pi / 180) * 55,
        )
        np.testing.assert_array_equal(scene.Earth.pos.np_vector, expected_position.np_vector)

    def test_get_star_nearest_to(self):
        scene = Scene()

        star = Star(
            name="Beta", hd_number="HD67890", longitude=10.0, latitude=20.0,
            init_year=2000, move_longitude_seconds=0.1, move_latitude_seconds=0.1,
            magnitude=5, spectral_class="K", reference={}, constellation_name=""
        )
        scene._filtered_stars.append(star)

        ray = PointVector(1.0, 1.0, 1.0)
        nearest_star = scene._get_star_nearest_to(ray)

        self.assertEqual(nearest_star, star)


if __name__ == '__main__':
    unittest.main()
