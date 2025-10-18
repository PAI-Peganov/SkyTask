from src.sky_and_stars_imports import *
from basic_shapes import *
from star_parser import parse_star_data_from_zip


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
        self._entities = []

    def get_entities(self):
        return self._entities.copy()

    def add_stars_from_zip(self, path: Path):
        data_stars = parse_star_data_from_zip(path)
        for star_data in data_stars:
            new_star = Star(
                name=star_data["name"],

            )
            self._entities.append(new_star)
