from src.shape_opengl_drawers import *
from src.point_vector import PointVector
import numpy as np
import datetime
import math


class BasicShape:
    def __init__(self, name: str):
        self.name = name

    def draw_shape(self):
        pass

        
class Star(BasicShape):
    def __init__(
            self,
            name: str,
            hd_number: int,
            longitude: float,
            latitude: float,
            init_date: datetime.date,
            move_longitude_seconds: float,
            move_latitude_seconds: float,
            spectral_class: str,
            reference: dict,
            constellation_name: str = None
    ):
        super().__init__(name)
        self.hd_number = hd_number
        self.longitude = longitude
        self.latitude = latitude
        self.init_date = init_date
        self.move_longitude = move_longitude_seconds / 3600
        self.move_latitude = move_latitude_seconds / 3600
        self._size_d = 7
        self.size = 0
        self.color = [0.0, 0.0, 0.0, 0.0]
        self._set_size_and_color_by(spectral_class)
        self.reference = reference
        self.constellation_name = constellation_name
        self.position = None
        self.set_time_span(init_date)

    def _set_size_and_color_by(self, spectral_class: str) -> None:
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
        if "III" in spectral_class:
            self.size = self._size_d - 3
        elif "IV" in spectral_class:
            self.size = self._size_d - 4
        elif "V" in spectral_class:
            self.size = self._size_d - 5
        elif "II" in spectral_class:
            self.size = self._size_d - 2
        elif "I" in spectral_class:
            self.size = self._size_d - 1
        else:
            raise ValueError("Unmatched star spectral class")

    def _get_size_by(self, lightning_class: str) -> float:
        match lightning_class:
            case "I": return self._size_d - 1
            case "II": return self._size_d - 2
            case "III": return self._size_d - 3
            case "IV": return self._size_d - 4
            case "V": return self._size_d - 5
        return self._size_d - 6

    def set_time_span(self, date: datetime.date) -> None:
        delta_years = (date - self.init_date).days / 365.25
        lon = (
            self.longitude + delta_years * self.move_longitude
        ) * math.pi / 180
        lat = (
            self.latitude + delta_years * self.move_latitude
        ) * math.pi / 180
        dist = 40
        self.position = PointVector(
            dist * math.cos(lon) * math.cos(lat),
            dist * math.sin(lon) * math.cos(lat),
            dist * math.sin(lat),
        )

    def get_position_numpy(self) -> np.array:
        return self.position.np_vector

    def draw_shape(self) -> None:
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
        self.color_active = []
        self.color_inactive = []
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

    def draw_shape(self):
        draw_constellation(self, self._get_color())
