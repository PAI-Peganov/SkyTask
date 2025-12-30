#!/usr/bin/env python3

from src.sky_and_stars_imports import *
from src.gl_widget import GLWidget
from src.scene_base import Scene
from src.point_vector import PointVector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = Scene()
        self.scene.add_stars_and_constellations_from_files(
            Path("src/stars.zip"), Path("src/constellations_dictionary.json")
        )
        self.openGL_widget = GLWidget(scene=self.scene, parent=self)
        uic.loadUi("src/untitled.ui", self)
        self.setWindowTitle("Sky And Stars")
        self.OpenGLContainer.layout().addWidget(self.openGL_widget)
        self._init_manage()

    def _init_manage(self):
        def params_set():
            self.scene.set_magnitude_filter_range(
                self.double_set_magn_min.value(),
                self.double_set_magn_max.value()
            )
            self.scene.set_position_on_earth(
                self.double_set_pos_latitude.value(),
                self.double_set_pos_longitude.value()
            )
            self.scene.set_year(self.double_set_year.value())
        self.button_apply.clicked.connect(params_set)

        self.double_set_view_latitude.valueChanged.connect(
            self.set_camera_lifting
        )
        self.double_set_view_longitude.valueChanged.connect(
            self.set_camera_rotation
        )
        self.double_set_view_fov.valueChanged.connect(
            self.set_camera_distance
        )

    def set_camera_rotation(self, angle):
        self.openGL_widget.camera_rotation_angle = (
                math.pi * angle / 180 % (2 * math.pi)
        )

    def set_camera_lifting(self, angle):
        self.openGL_widget.camera_lifting_angle = math.pi * angle / 180

    def set_camera_distance(self, distance):
        self.openGL_widget.camera_fov_angle = distance


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
