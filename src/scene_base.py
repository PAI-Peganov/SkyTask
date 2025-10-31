from src.sky_and_stars_imports import *
from basic_shapes import *
from star_parser import parse_star_data_from_zip
import numpy as np
import math


class EntityNotFoundException(Exception):
    def __init__(self, name):
        super().__init__("Указана несуществующая сущьность {}".format(name))


class EntityWrongTypeException(Exception):
    def __init__(self, name, expected_type, entity_type):
        super().__init__(
            "{} должна быть {}, а является {}".format(
                name, expected_type, entity_type
            )
        )


class EmptyFieldException(Exception):
    def __init__(self):
        super().__init__("В поле ничего не указано")


class EntityNameAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("Сущьность с таким именем уже существует")


class Scene:
    def __init__(self, app_update: callable):
        self.app_update = app_update
        self._scene_time = None
        self._stars = []
        self._constellations = []
        self._active_constellation = None

    def get_entities(self):
        for s in self._stars:
            yield s
        for c in self._constellations:
            yield c

    def add_stars_from_zip(self, path: Path):
        data_stars = parse_star_data_from_zip(path)
        for star_data in data_stars:
            lon = star_data["galactic_lon"] * math.pi / 180
            lat = star_data["galactic_lat"] * math.pi / 180
            dist = 40
            position = PointVector(
                dist * math.cos(lon) * math.cos(lat),
                dist * math.sin(lon) * math.cos(lat),
                dist * math.sin(lat)
            )
            new_star = Star(
                name=star_data["name"],
                hd_number=star_data["id"],
                position=position,
            )
            self._stars.append(new_star)

    def get_star_and_constellation_nearest_to(self, ray: PointVector):
        star = self._get_star_nearest_to(ray)
        if self._active_constellation is not None:
            self._active_constellation.set_picked(False)
        self._active_constellation = self._get_constellation_by(star)
        if self._active_constellation is not None:
            self._active_constellation.set_picked(True)

    def _get_star_nearest_to(self, ray: PointVector):
        np_ray = ray.np_vector / np.linalg.norm(ray.np_vector)
        return max(
            (
                np.dot(
                    np_ray,
                    (p := s.get_position_numpy()) / np.linalg.norm(p)
                ),
                s
            )
            for s in self._stars
        )[1]

    def _get_constellation_by(self, star: Star):
        for ent in self._constellations:
            if ent is Constellation and ent.name == star.constellation_name:
                return ent
        return None
