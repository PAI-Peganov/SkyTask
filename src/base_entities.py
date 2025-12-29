from src.shape_opengl_drawers import *
from src.point_vector import PointVector
import numpy as np
import math


class BasicEntity:
    def __init__(self, name: str):
        self.name = name

    def draw_shape(self):
        pass

        
class Star(BasicEntity):
    def __init__(
            self,
            name: str,
            hd_number: str,
            longitude: float,
            latitude: float,
            init_year: int,
            move_longitude_seconds: float,
            move_latitude_seconds: float,
            magnitude: float,
            spectral_class: str,
            reference: dict,
            constellation_name: str = None
    ):
        super().__init__(name)
        self.hd_number = hd_number
        self.longitude = longitude  # Долгота
        self.latitude = latitude  # Широта
        self.init_year = init_year
        self.move_longitude = move_longitude_seconds / 3600
        self.move_latitude = move_latitude_seconds / 3600
        self.magnitude = magnitude
        self._size_d = 7
        self.size = (self._size_d - magnitude) * 1.5
        self.color = [0.0, 0.0, 0.0, 0.0]
        self._set_color_by(spectral_class)
        self.reference = reference
        self.constellation_name = constellation_name
        self.position = None
        self.set_time_span(init_year)

    def _set_color_by(self, spectral_class: str) -> None:
        temp_class_letter = spectral_class[0]
        if temp_class_letter == "g":
            temp_class_letter = spectral_class[1]
        match temp_class_letter:
            case "O": self.color = [0.2, 0.5, 1.0, 1.0]
            case "B": self.color = [0.5, 0.8, 1.0, 1.0]
            case "A": self.color = [1.0, 1.0, 1.0, 1.0]
            case "F": self.color = [1.0, 1.0, 0.4, 1.0]
            case "G": self.color = [1.0, 1.0, 0.2, 1.0]
            case "K": self.color = [1.0, 0.6, 0.2, 1.0]
            case "M": self.color = [1.0, 0.2, 0.2, 1.0]
        # if "III" in spectral_class:
        #     self.size = self._size_d - 3
        # elif "IV" in spectral_class:
        #     self.size = self._size_d - 4
        # elif "V" in spectral_class:
        #     self.size = self._size_d - 5
        # elif "II" in spectral_class:
        #     self.size = self._size_d - 2
        # elif "I" in spectral_class:
        #     self.size = self._size_d - 1
        # else:
        #     self.size = 0
        #     print(f"Unmatched star spectral class: {spectral_class}")

    def set_time_span(self, year: int) -> None:
        delta_years = year - self.init_year
        lon = (
            self.longitude + delta_years * self.move_longitude
        ) * math.pi / 180
        lat = (
            self.latitude + delta_years * self.move_latitude
        ) * math.pi / 180
        dist = 40
        self.position = PointVector(
            dist * math.cos(lat) * math.cos(lon),
            dist * math.cos(lat) * math.sin(lon),
            dist * math.sin(lat),
        )

    def get_position_numpy(self) -> np.array:
        return self.position.np_vector

    def draw_shape(self) -> None:
        if self.size > 0:
            pos = self.get_position_numpy()
            draw_point_param(pos, self.size, self.color)
            draw_point_param(
                pos * 0.99, self.size * 0.5, [1.0, 1.0, 1.0, 1.0]
            )

    def __eq__(self, other):
        return self.hd_number == other.hd_number

    def __gt__(self, other):
        return self.constellation_name is not None

    def __hash__(self):
        return self.hd_number.__hash__()


class Segment(BasicEntity):
    def __init__(self, name: str, a: PointVector, b: PointVector):
        super().__init__(name)
        self.point_a = a
        self.point_b = b

    def draw_shape(self):
        draw_segment(self)


class Constellation(BasicEntity):
    def __init__(self, name: str, star_polylines: list[list[Star]]):
        super().__init__(name)
        self.star_polylines = star_polylines
        self.stars = set(star for poly in star_polylines for star in poly)
        self.color_active = [0.3, 0.3, 0.3, 1.0]
        self.color_inactive = [0.2, 0.2, 0.2, 1.0]
        self.is_picked = False

    def contains(self, star: Star) -> bool:
        for s in self.stars:
            if s.hd_number == star.hd_number:
                return True
        return False

    def _get_color(self):
        if self.is_picked:
            return self.color_active
        return self.color_inactive

    def set_picked(self, picked: bool):
        self.is_picked = picked

    def draw_shape(self):
        for polyline in self.star_polylines:
            draw_polyline(polyline, self._get_color())


class Earth(BasicEntity):
    def __init__(self, name: str = "Earth"):
        super().__init__(name)
        self.pos = PointVector(-55, 0, 0)

    def draw_shape(self):
        draw_earth(self)
