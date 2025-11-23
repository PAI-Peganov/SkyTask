from src.sky_and_stars_imports import *
from base_entities import *
from star_parser import parse_star_data_from_zip
import numpy as np


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
    def __init__(self, app_update: callable = datetime.datetime.now):
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
            new_star = Star(
                name=star_data["name"],
                hd_number=star_data["id"],
                longitude=star_data["galactic_lon"],
                latitude=star_data["galactic_lat"],
                init_year=2025,
                move_longitude_seconds=star_data["move_longitude"],
                move_latitude_seconds=star_data["move_latitude"],
                spectral_class=star_data["spectral_class"],
                reference=star_data,
                constellation_name="",
            )
            self._stars.append(new_star)
        print(len(self._stars))

    def set_year(self, year: float):
        for star in self._stars:
            star.set_time_span(int(year))

    def get_star_and_constellation_nearest_to(self, ray: PointVector):
        star = self._get_star_nearest_to(ray)
        if star is None:
            return None
        self._try_set_active_constellation_pick(False)
        self._active_constellation = self._get_constellation_by(star)
        self._try_set_active_constellation_pick(True)
        return star

    def _try_set_active_constellation_pick(self, is_picked: bool) -> bool:
        if self._active_constellation is not None:
            self._active_constellation.set_picked(is_picked)
            return True
        return False

    def _get_star_nearest_to(self, ray: PointVector):
        np_ray = ray.np_vector
        np_ray /= np.linalg.norm(np_ray)
        nearest_star = max(map(
            lambda s: (np.dot(np_ray, s.get_position_numpy()), s),
            self._stars
        ))
        if nearest_star[0] > 0.5 * np.linalg.norm(
            nearest_star[1].get_position_numpy()
        ):
            return nearest_star[1]
        return None

    def _get_constellation_by(self, star: Star):
        for ent in self._constellations:
            if ent is Constellation and ent.name == star.constellation_name:
                return ent
        return None
