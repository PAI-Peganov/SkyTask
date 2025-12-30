import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import json
from src.star_parser import *


class TestStarDataFunctions(unittest.TestCase):

    def test_build_star_data_valid(self):
        line_data = " 95  4: 7: 0.5 +29: 0: 5 166.46 -16.90    5.23   F1V                -0.092 +0.007       +009  25867  42Psi "

        expected_result = {
            "id": "42Psi",
            "longitude": "4: 7: 0.5",
            "latitude": "+29: 0: 5",
            "galactic_lon": 166.46,
            "galactic_lat": -16.9,
            "magnitude": 5.23,
            "spectral_class": "F1V",
            "move_longitude": -0.092,
            "move_latitude": 0.007,
            "additional_nums": [9],
            "name": "Psi"
        }

        result = build_star_data(line_data)
        self.assertEqual(result, expected_result)

    def test_build_star_data_invalid(self):
        line_data = "Invalid star data string"

        result = build_star_data(line_data)
        self.assertIsNone(result)

    @patch('zipfile.ZipFile')
    def test_parse_star_data_from_zip(self, MockZipFile):
        mock_zip = mock_open(
            read_data="95  4: 7: 0.5 +29: 0: 5 166.46 -16.90    5.23   F1V                -0.092 +0.007       +009  25867  42Psi ")
        MockZipFile.return_value.__enter__.return_value = mock_zip

        path = Path("test.zip")
        result = parse_star_data_from_zip(path)

        expected_result = [{
            "id": "25867",
            "longitude": "4: 7: 0.5",
            "latitude": "+29: 0: 5",
            "galactic_lon": 166.46,
            "galactic_lat": -16.9,
            "magnitude": 5.23,
            "spectral_class": "F1V",
            "move_longitude": -0.092,
            "move_latitude": 0.007,
            "additional_nums": [9],
            "name": "42Psi"
        }]
        self.assertEqual(result, expected_result)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(
        {"constellation1": {"name": "Orion", "stars": ["Betelgeuse"]}}))
    def test_parse_constellation_data_from_json(self, mock_file):
        path = Path("constellations.json")
        result = parse_constellation_data_from_json(path)

        expected_result = [{"name": "Orion", "stars": ["Betelgeuse"]}]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
