from src.sky_and_stars_imports import *
from base_entities import *
from star_parser import parse_star_data_from_zip
import numpy as np


class Scene:
    def __init__(self, app_update: callable = datetime.datetime.now):
        self.app_update = app_update
        self._scene_time = None
        self._stars = []
        self._filtered_stars = []
        self._constellations = []
        self._active_star = None
        self._active_constellation = None
        self._magnitude_min = -2
        self._magnitude_max = 6
        self.Earth = Earth()

    def get_entities(self):
        for s in self._filtered_stars:
            yield s
        for c in self._constellations:
            yield c
        yield self.Earth

    def _add_stars_from_zip(self, path: Path):
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
                magnitude=star_data["magnitude"],
                spectral_class=star_data["spectral_class"],
                reference=star_data,
                constellation_name="",
            )
            self._stars.append(new_star)
        self._update_filtered_list_stars()
        print(len(self._stars))

    def _update_filtered_list_stars(self):
        self._filtered_stars = []
        for star in self._stars:
            if self._magnitude_min <= star.magnitude <= self._magnitude_max:
                self._filtered_stars.append(star)

    def set_magnitude_filter_range(self, min_value: int, max_value: int):
        self._magnitude_min = min_value
        self._magnitude_max = max_value
        self._update_filtered_list_stars()

    def set_position_on_earth(self, latitude: float, longitude: float):
        self.Earth.pos = PointVector(
            math.cos(longitude * math.pi / 180 + math.pi) *
            math.cos(-latitude * math.pi / 180) * 55,
            math.sin(longitude * math.pi / 180 + math.pi) *
            math.cos(-latitude * math.pi / 180) * 55,
            math.sin(-latitude * math.pi / 180) * 55,
        )

    def _add_constellations_from_json(self, path: Path):
        data_constellations = parse_constellation_data_from_json(path)
        for data_con in data_constellations:
            star_polylines = []
            for data_poly in data_con["lines"]:
                star_poly = []
                for star_hd in data_poly:
                    if star_hd is None:
                        continue
                    found = [x for x in self._stars if x.hd_number == star_hd]
                    if len(found) > 0:
                        star_poly.append(found[0])
                        found[0].constellation_name = data_con["name"]
                star_polylines.append(star_poly)
            self._constellations.append(
                Constellation(
                    name=data_con["name"],
                    star_polylines=star_polylines
                )
            )

    def add_stars_and_constellations_from_files(
            self, path_stars: Path, path_con: Path
    ):
        self._add_stars_from_zip(path_stars)
        self._add_constellations_from_json(path_con)

    def set_year(self, year: float):
        for star in self._stars:
            star.set_time_span(int(year))

    def set_active_star_and_constellation_nearest_to(self, ray: PointVector):
        star = self._get_star_nearest_to(ray)
        if star is None:
            return None
        self._try_set_active_constellation_pick(False)
        self._active_constellation = self._get_constellation_by(star)
        self._try_set_active_constellation_pick(True)
        return star, self._active_constellation

    def _try_set_active_constellation_pick(self, is_picked: bool) -> bool:
        if self._active_constellation is not None:
            self._active_constellation.set_picked(is_picked)
            return True
        return False

    def _get_star_nearest_to(self, ray: PointVector):
        np_ray = ray.np_vector
        np_ray /= np.linalg.norm(np_ray)
        nearest_star = max(map(
            lambda s: (
                np.dot(np_ray, s.get_position_numpy()) / np.linalg.norm(
                    s.get_position_numpy()
                ),
                s
            ),
            self._filtered_stars
        ))
        if nearest_star[0] > 0.95:
            return nearest_star[1]
        return None

    def _get_constellation_by(self, star: Star):
        for con in self._constellations:
            if con.name == star.constellation_name:
                return con
        return None
