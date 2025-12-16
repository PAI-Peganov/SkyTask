#!/usr/bin/env python3

from src.sky_and_stars_imports import *
from src.gl_widget import GLWidget
from src.scene_base import Scene
from src.adding_windows import *
from src.point_vector import PointVector
from OpenGL.GLUT import *
from tkinter import filedialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.scene = Scene(self.scene_update)
        self.scene = Scene()
        self.scene.add_stars_and_constellations_from_files(
            Path("src/stars.zip"), Path("src/constellations_dictionary.json")
        )
        self.openGL_widget = GLWidget(scene=self.scene)
        uic.loadUi("src/untitled.ui", self)
        self.setWindowTitle("Sky And Stars")
        self.OpenGLContainer.layout().addWidget(self.openGL_widget)
        # self.init_scene()

    # def init_tree_interaction(self):
    #     def tree_clicked(item, column):
    #         entity = self.scene._entities[item.text(0)]
    #         options = entity.get_edit_params()
    #         self.label_name_view.setText(entity.name)
    #         self.double_edit_x.setValue(entity.x)
    #         self.double_edit_y.setValue(entity.y)
    #         self.double_edit_z.setValue(entity.z)
    #
    #         def apply_clicked():
    #             values = {
    #                 "x": float(self.double_edit_x.value()),
    #                 "y": float(self.double_edit_y.value()),
    #                 "z": float(self.double_edit_z.value()),
    #                 "upd": self.openGL_widget.get_frame_count_since_startup()
    #             }
    #             options[1](**values)
    #             self.double_edit_x.setValue(entity.x)
    #             self.double_edit_y.setValue(entity.y)
    #             self.double_edit_z.setValue(entity.z)
    #
    #         self.button_edit_apply.clicked.connect(apply_clicked)
    #
    #     self.entity_tree.itemClicked.connect(tree_clicked)
    #
    # def init_saving_field(self):
    #     layout = QHBoxLayout()
    #     path_line = QLineEdit()
    #
    #     def save_click():
    #         save_path = path_line.text().strip()
    #         if not save_path:
    #             save_path = filedialog.asksaveasfilename(
    #                 defaultextension=".pkl",
    #                 filetypes=[("Pickle files", "*.pkl")]
    #             )
    #         if save_path:
    #             self.scene.save_entities_to_file(Path(save_path))
    #             path_line.setText(str(Path(save_path)))
    #     save_button = QPushButton(text="Save")
    #     save_button.clicked.connect(save_click)
    #
    #     def load_click():
    #         load_path = filedialog.askopenfilename(
    #             filetypes=[("Pickle files", "*.pkl")]
    #         )
    #         if load_path:
    #             if not os.path.exists(load_path):
    #                 QMessageBox.warning(self, "Ошибка", "Файл не найден")
    #             self.scene.load_entities_from_file(Path(load_path))
    #             path_line.setText(str(Path(load_path)))
    #     load_button = QPushButton(text="Load")
    #     load_button.clicked.connect(load_click)
    #
    #     def save_frame():
    #         picture_path = filedialog.asksaveasfilename(
    #             defaultextension=".png",
    #             filetypes=[("Picture PNG", "*.png")]
    #         )
    #         if picture_path:
    #             self.openGL_widget.save_to_png(Path(picture_path))
    #     shoot_button = QPushButton(text="ScreenShoot")
    #     shoot_button.clicked.connect(save_frame)
    #
    #     layout.addWidget(shoot_button)
    #     layout.addWidget(load_button)
    #     layout.addWidget(path_line)
    #     layout.addWidget(save_button)
    #     self.widget.layout().addLayout(layout)
    #
    # def init_scroll(self):
    #     self.scroll_rotation.setRange(-120, 360)
    #     self.scroll_rotation.setValue(0)
    #     self.scroll_rotation.valueChanged.connect(self.set_camera_rotation)
    #     self.scroll_lifting.setRange(-90, 90)
    #     self.scroll_lifting.setValue(-20)
    #     self.scroll_lifting.valueChanged.connect(self.set_camera_lifting)
    #     self.scroll_zooming.setRange(1, 20)
    #     self.scroll_zooming.setValue(self.openGL_widget.camera_fov_angle)
    #     self.scroll_zooming.valueChanged.connect(self.set_camera_distance)
    #     self.spinbox_zooming.setRange(1, 300)
    #     self.spinbox_zooming.setValue(self.openGL_widget.camera_fov_angle)
    #     self.spinbox_zooming.setSingleStep(0.05)
    #     self.spinbox_zooming.valueChanged.connect(self.set_camera_distance)
    #     layout = QHBoxLayout()
    #     layout.addLayout(QVBoxLayout())
    #     layout.addWidget(self.spinbox_zooming)
    #     self.widget.layout().addLayout(layout)

    def set_camera_rotation(self, angle):
        self.openGL_widget.camera_rotation_angle = math.pi * angle / 180

    def set_camera_lifting(self, angle):
        self.openGL_widget.camera_lifting_angle = -math.pi * angle / 180

    def set_camera_distance(self, distance):
        if distance >= self.scroll_zooming.maximum():
            self.scroll_zooming.setRange(1, distance + 1)
            self.spinbox_zooming.setRange(
                1, max(distance + 1, self.spinbox_zooming.maximum())
            )
        self.openGL_widget.camera_fov_angle = distance
        self.scroll_zooming.setValue(int(distance))
        self.spinbox_zooming.setValue(float(distance))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
