from src.sky_and_stars_imports import *


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
        self._entities = dict()

    def get_entities(self):
        return self._entities.values()

    def load_entities_from_file(self, filepath: Path):
        if filepath.suffix != ".pkl":
            raise TypeError("file is not .pkl")
        with open(filepath, 'rb') as f:
            self._entities = pickle.load(f)
        for el in self._entities.values():
            el.last_update = 0
        self.app_update()

    def check_contains_errors(self, *args, new_entity=None):
        for el in args:
            if len(el[0]) == 0:
                raise EmptyFieldException()
            if self._entities.get(el[0]) is None:
                raise EntityNotFoundException(el[0])
            if not isinstance(self._entities.get(el[0]), el[1]):
                raise EntityWrongTypeException(
                    el[0], el[1], type(self._entities.get(el[0]))
                )
        if new_entity is not None:
            if len(new_entity) == 0:
                raise EmptyFieldException()
            if self._entities.get(new_entity) is not None:
                raise EntityNameAlreadyExistsException()

    def add_point(self, name: str, x: float, y: float, z: float):
        self.check_contains_errors(new_entity=name)
        self._entities[name] = Point(name, x, y, z)
        self.app_update()

    def add_light(self, name: str, lightGL, x: float, y: float, z: float):
        self._entities[name] = LightPoint(name, lightGL, x, y, z)
        self.app_update()

    def add_segment(self, name: str, point_a_name: str, point_b_name: str):
        self.check_contains_errors(
            (point_a_name, Point), (point_b_name, Point), new_entity=name
        )
        self._entities[name] = Segment(
            name, self._entities[point_a_name], self._entities[point_b_name]
        )
        self._entities[name].add_children([point_a_name, point_b_name])
        self.app_update()
