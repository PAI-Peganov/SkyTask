from src.simple_3d_editor_imports import *
import unittest
from unittest.mock import MagicMock


class TestExceptions(unittest.TestCase):
    def test_entity_not_found_exception(self):
        with self.assertRaises(EntityNotFoundException) as context:
            raise EntityNotFoundException("test_entity")
        self.assertEqual(
            str(context.exception),
            "Указана несуществующая сущьность test_entity"
        )

    def test_entity_wrong_type_exception(self):
        with self.assertRaises(EntityWrongTypeException) as context:
            raise EntityWrongTypeException("test_entity", "Point", "Segment")
        self.assertEqual(
            str(context.exception),
            "test_entity должна быть Point, а является Segment"
        )

    def test_empty_field_exception(self):
        with self.assertRaises(EmptyFieldException) as context:
            raise EmptyFieldException()
        self.assertEqual(str(context.exception), "В поле ничего не указано")

    def test_entity_name_already_exists_exception(self):
        with self.assertRaises(EntityNameAlreadyExistsException) as context:
            raise EntityNameAlreadyExistsException()
        self.assertEqual(
            str(context.exception), "Сущьность с таким именем уже существует"
        )


class TestScene(unittest.TestCase):
    def setUp(self):
        self.mock_update = MagicMock()
        self.scene = Scene(self.mock_update)

    def test_initialization(self):
        self.assertIsNone(self.scene.path)
        self.assertEqual(self.scene.app_update, self.mock_update)
        self.assertEqual(self.scene.entities, {})
        self.assertEqual(len(self.scene.stack_last_actions), 0)
        self.assertEqual(len(self.scene.stack_undo_actions), 0)

    # @patch('builtins.open')
    # @patch('pickle.load')
    # def test_load_entities_from_file(self, mock_pickle_load, mock_open):
    #     mock_pickle_load.return_value = {'test': 'entity'}
    #     self.scene.load_entities_from_file(Path("test.pkl"))
    #     mock_open.assert_called_once_with(Path("test.pkl"), 'rb')
    #     self.assertEqual(self.scene.entities, {'test': 'entity'})
    #     self.mock_update.assert_called_once()
    #
    # @patch('builtins.open')
    # @patch('pickle.dump')
    # def test_save_entities_to_file(self, mock_pickle_dump, mock_open):
    #     self.scene.entities = {'test': 'entity'}
    #     self.scene.save_entities_to_file(Path("test.pkl"))
    #     mock_open.assert_called_once_with(Path("test.pkl"), 'wb')
    #     mock_pickle_dump.assert_called_once_with(
    #         {'test': 'entity'}, mock_open.return_value
    #     )

    def test_check_contains_errors_empty_field(self):
        with self.assertRaises(EmptyFieldException):
            self.scene.check_contains_errors(("", Point))

    def test_check_contains_errors_entity_not_found(self):
        with self.assertRaises(EntityNotFoundException):
            self.scene.check_contains_errors(("nonexistent", Point))

    def test_check_contains_errors_wrong_type(self):
        self.scene.entities['test'] = "not_a_point"
        with self.assertRaises(EntityWrongTypeException):
            self.scene.check_contains_errors(("test", Point))

    def test_check_contains_errors_name_exists(self):
        self.scene.entities['existing'] = "something"
        with self.assertRaises(EntityNameAlreadyExistsException):
            self.scene.check_contains_errors(new_entity="existing")

    def test_add_point(self):
        self.scene.add_point("test_point", 1.0, 2.0, 3.0)
        self.assertIn("test_point", self.scene.entities)
        self.mock_update.assert_called_once()

    def test_add_light(self):
        self.scene.add_light("test_light", "lightGL", 1.0, 2.0, 3.0)
        self.assertIn("test_light", self.scene.entities)
        self.mock_update.assert_called_once()

    def test_add_segment(self):
        self.scene.add_point("point_a", 0.0, 0.0, 0.0)
        self.scene.add_point("point_b", 1.0, 1.0, 1.0)
        self.scene.add_segment("test_segment", "point_a", "point_b")
        self.assertIn("test_segment", self.scene.entities)
        self.mock_update.assert_called()

    def test_add_figure2(self):
        self.scene.add_point("point1", 0.0, 0.0, 0.0)
        self.scene.add_point("point2", 1.0, 0.0, 0.0)
        self.scene.add_point("point3", 0.5, 1.0, 0.0)
        self.scene.add_figure2("test_figure", ["point1", "point2", "point3"])
        self.assertIn("test_figure", self.scene.entities)
        self.mock_update.assert_called()

    def test_add_figure2_n(self):
        self.scene.add_figure2_n("test_figure", 4, 1.0)
        self.assertIn("test_figure", self.scene.entities)
        self.assertEqual(
            len([k for k in self.scene.entities.keys()
                 if k.startswith("figure2_point_test_figure_")]), 4
        )
        self.mock_update.assert_called()

    def test_add_plane_by_points(self):
        self.scene.add_point("point1", 0.0, 0.0, 0.0)
        self.scene.add_point("point2", 1.0, 0.0, 0.0)
        self.scene.add_point("point3", 0.0, 1.0, 0.0)
        self.scene.add_plane_by_points(
            "test_plane", "point1", "point2", "point3"
        )
        self.assertIn("test_plane", self.scene.entities)
        self.mock_update.assert_called()

    def test_add_plane_by_point_and_segment(self):
        self.scene.add_point("point1", 0.0, 0.0, 0.0)
        self.scene.add_point("point2", 1.0, 0.0, 0.0)
        self.scene.add_point("point3", 0.0, 1.0, 0.0)
        self.scene.add_segment("test_segment", "point2", "point3")
        self.scene.add_plane_by_point_and_segment(
            "test_plane", "point1", "test_segment"
        )
        self.assertIn("test_plane", self.scene.entities)
        self.mock_update.assert_called()

    def test_add_plane_by_plane(self):
        self.scene.add_point("point1", 0.0, 0.0, 0.0)
        self.scene.add_point("point2", 1.0, 0.0, 0.0)
        self.scene.add_point("point3", 0.0, 1.0, 0.0)
        self.scene.add_plane_by_points(
            "base_plane", "point1", "point2", "point3"
        )
        self.scene.add_point("new_point", 0.0, 0.0, 1.0)
        self.scene.add_plane_by_plane("test_plane", "new_point", "base_plane")
        self.assertIn("test_plane", self.scene.entities)
        self.mock_update.assert_called()

    def test_add_contur_to_plane(self):
        self.scene.add_point("point1", 0.0, 0.0, 0.0)
        self.scene.add_point("point2", 1.0, 0.0, 0.0)
        self.scene.add_point("point3", 0.0, 1.0, 0.0)
        self.scene.add_plane_by_points(
            "test_plane", "point1", "point2", "point3"
        )
        self.scene.add_segment("segment1", "point1", "point2")
        self.scene.add_segment("segment2", "point2", "point3")
        self.scene.add_segment("segment3", "point3", "point1")
        self.scene.add_contur_to_plane(
            "test_plane", ["segment1", "segment2", "segment3"]
        )
        self.assertEqual(len(self.scene.entities["test_plane"].contur), 1)
        self.mock_update.assert_called()

    def test_add_contur_n_to_plane(self):
        self.scene.add_point("point1", 0.0, 0.0, 0.0)
        self.scene.add_point("point2", 1.0, 0.0, 0.0)
        self.scene.add_point("point3", 0.0, 1.0, 0.0)
        self.scene.add_plane_by_points(
            "test_plane", "point1", "point2", "point3"
        )
        self.scene.add_contur_n_to_plane("test_plane", 4, 1.0)
        self.assertEqual(len(self.scene.entities["test_plane"].contur), 1)
        self.mock_update.assert_called()

    def test_add_figure3(self):
        self.scene.add_point("point1", 0.0, 0.0, 0.0)
        self.scene.add_point("point2", 1.0, 0.0, 0.0)
        self.scene.add_point("point3", 0.5, 1.0, 0.0)
        self.scene.add_figure2("face1", ["point1", "point2", "point3"])
        self.scene.add_figure3("test_figure3", ["face1"])
        self.assertIn("test_figure3", self.scene.entities)
        self.mock_update.assert_called()

    def test_add_prism_n(self):
        self.scene.add_prism_n("test_prism", 4, 1.0, 2.0)
        self.assertIn("test_prism", self.scene.entities)
        self.assertEqual(
            len([k for k in self.scene.entities.keys()
                 if k.startswith("pnt_upr_test_prism_")]), 4
        )
        self.assertEqual(
            len([k for k in self.scene.entities.keys()
                 if k.startswith("pnt_lwr_test_prism_")]), 4
        )
        self.mock_update.assert_called()

    def test_add_pyramid_n(self):
        self.scene.add_pyramid_n("test_pyramid", 4, 1.0, 2.0)
        self.assertIn("test_pyramid", self.scene.entities)
        self.assertEqual(
            len([k for k in self.scene.entities.keys()
                 if k.startswith("pnt_lwr_test_pyramid_")]), 4
        )
        self.assertIn("pnt_upr_test_pyramid", self.scene.entities)
        self.mock_update.assert_called()

    def test_add_sphere_nm(self):
        self.scene.add_sphere_nm("test_sphere", 4, 3, 1.0)
        self.assertIn("test_sphere", self.scene.entities)
        self.assertIn("pnt_up_test_sphere", self.scene.entities)
        self.assertIn("pnt_down_test_sphere", self.scene.entities)
        self.mock_update.assert_called()


class TestCollinearCheck(unittest.TestCase):
    def test_is_point_collinear_true(self):
        p1 = MagicMock(x=0.0, y=0.0, z=0.0)
        p2 = MagicMock(x=1.0, y=0.0, z=0.0)
        p3 = MagicMock(x=2.0, y=0.0, z=0.0)
        self.assertTrue(is_point_collinear(p1, p2, p3))

    def test_is_point_collinear_false(self):
        p1 = MagicMock(x=0.0, y=0.0, z=0.0)
        p2 = MagicMock(x=1.0, y=0.0, z=0.0)
        p3 = MagicMock(x=0.0, y=1.0, z=0.0)
        self.assertFalse(is_point_collinear(p1, p2, p3))

    def test_is_point_collinear_less_than_3_points(self):
        p1 = MagicMock(x=0.0, y=0.0, z=0.0)
        p2 = MagicMock(x=1.0, y=0.0, z=0.0)
        self.assertTrue(is_point_collinear(p1, p2))


if __name__ == '__main__':
    unittest.main()
