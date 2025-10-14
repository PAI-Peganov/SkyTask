#!/usr/bin/env python3

from src.simple_3d_editor_imports import *
from tkinter import filedialog


class GLWidget(QGLWidget):
    def __init__(self, parent=None, scene=None):
        super(GLWidget, self).__init__(parent)
        self.scene = scene
        self.camera_rotation_angle = 0
        self.camera_lifting_angle = math.pi / 9
        self.camera_distance = 5
        self.frame_counter = 0
        self.basis_p_0 = Point("", 0, 0, 0)
        self.basis_p_x = Point("", 1, 0, 0)
        self.basis_p_y = Point("", 0, 1, 0)
        self.basis_p_z = Point("", 0, 0, 1)
        self.basis_x = Segment("", self.basis_p_x, self.basis_p_0)
        self.basis_y = Segment("", self.basis_p_y, self.basis_p_0)
        self.basis_z = Segment("", self.basis_p_z, self.basis_p_0)
        self.basis_render_size = 0.3

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0, 0, 0, 1.0)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [1.0, 1.0, 1.0, 1])
        # Настройка источника света
        # Направленный свет
        # glLightfv(GL_LIGHT0, GL_POSITION, [-100.0, 100.0, 100.0, 0.0])
        # Цвет рассеянного света
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        # Цвет зеркального отражения
        # glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        # включение нормалей
        glEnable(GL_NORMALIZE)
        # glLineWidth(2.0)
        # glEnable(GL_LINE_SMOOTH)
        # glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        # glPointSize(4.0)
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, self.width() / self.height(), 0.1, 100.0)
        gluLookAt(
            math.cos(self.camera_rotation_angle) *
            math.cos(self.camera_lifting_angle) * self.camera_distance,
            math.sin(self.camera_rotation_angle) *
            math.cos(self.camera_lifting_angle) * self.camera_distance,
            math.sin(self.camera_lifting_angle) * self.camera_distance,
            0, 0, 0,
            0, 0, 1
        )
        self.frame_counter += 1

        for name, entity in self.scene.entities.items():
            entity.draw_shape()

        self.update()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def save_to_png(self, filepath):
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        viewport = glGetIntegerv(GL_VIEWPORT)
        buffer = glReadPixels(
            0, 0, viewport[2], viewport[3], GL_RGB, GL_UNSIGNED_BYTE
        )
        image = Image.frombytes('RGB', (viewport[2], viewport[3]), buffer)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(str(filepath), format='PNG')

    def get_frame_count_since_startup(self):
        return self.frame_counter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = Scene(self.scene_update)

        self.openGL_widget = GLWidget(scene=self.scene)
        uic.loadUi("src/untitled.ui", self)
        self.setWindowTitle("SimpleBlender")
        self.OpenGLContainer.layout().addWidget(self.openGL_widget)

        self.adding_page.layout().addWidget(
            AddingOptionsWidget(
                "", self.init_adding_params(), is_destroyable=False
            )
        )
        self.entity_tree.setColumnCount(2)
        self.entity_tree.setHeaderLabels(["Имя", "Тип"])
        self.init_tree_interaction()
        self.spinbox_zooming = QDoubleSpinBox()
        self.init_scroll()
        self.init_saving_field()
        self.init_scene()

    def init_tree_interaction(self):
        def tree_clicked(item, column):
            entity = self.scene.entities[item.text(0)]
            options = entity.get_edit_params()
            self.label_name_view.setText(entity.name)
            self.double_edit_x.setValue(entity.x)
            self.double_edit_y.setValue(entity.y)
            self.double_edit_z.setValue(entity.z)

            def apply_clicked():
                values = {
                    "x": float(self.double_edit_x.value()),
                    "y": float(self.double_edit_y.value()),
                    "z": float(self.double_edit_z.value()),
                    "upd": self.openGL_widget.get_frame_count_since_startup()
                }
                options[1](**values)
                self.double_edit_x.setValue(entity.x)
                self.double_edit_y.setValue(entity.y)
                self.double_edit_z.setValue(entity.z)

            self.button_edit_apply.clicked.connect(apply_clicked)

        self.entity_tree.itemClicked.connect(tree_clicked)

    def init_saving_field(self):
        layout = QHBoxLayout()
        path_line = QLineEdit()

        def save_click():
            save_path = path_line.text().strip()
            if not save_path:
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".pkl",
                    filetypes=[("Pickle files", "*.pkl")]
                )
            if save_path:
                self.scene.save_entities_to_file(Path(save_path))
                path_line.setText(str(Path(save_path)))
        save_button = QPushButton(text="Save")
        save_button.clicked.connect(save_click)

        def load_click():
            load_path = filedialog.askopenfilename(
                filetypes=[("Pickle files", "*.pkl")]
            )
            if load_path:
                if not os.path.exists(load_path):
                    QMessageBox.warning(self, "Ошибка", "Файл не найден")
                self.scene.load_entities_from_file(Path(load_path))
                path_line.setText(str(Path(load_path)))
        load_button = QPushButton(text="Load")
        load_button.clicked.connect(load_click)

        def save_frame():
            picture_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("Picture PNG", "*.png")]
            )
            if picture_path:
                self.openGL_widget.save_to_png(Path(picture_path))
        shoot_button = QPushButton(text="ScreenShoot")
        shoot_button.clicked.connect(save_frame)

        layout.addWidget(shoot_button)
        layout.addWidget(load_button)
        layout.addWidget(path_line)
        layout.addWidget(save_button)
        self.widget.layout().addLayout(layout)

    def init_scroll(self):
        self.scroll_rotation.setRange(-120, 360)
        self.scroll_rotation.setValue(0)
        self.scroll_rotation.valueChanged.connect(self.set_camera_rotation)
        self.scroll_lifting.setRange(-90, 90)
        self.scroll_lifting.setValue(-20)
        self.scroll_lifting.valueChanged.connect(self.set_camera_lifting)
        self.scroll_zooming.setRange(1, 20)
        self.scroll_zooming.setValue(self.openGL_widget.camera_distance)
        self.scroll_zooming.valueChanged.connect(self.set_camera_distance)
        self.spinbox_zooming.setRange(1, 300)
        self.spinbox_zooming.setValue(self.openGL_widget.camera_distance)
        self.spinbox_zooming.setSingleStep(0.05)
        self.spinbox_zooming.valueChanged.connect(self.set_camera_distance)
        layout = QHBoxLayout()
        layout.addLayout(QVBoxLayout())
        layout.addWidget(self.spinbox_zooming)
        self.widget.layout().addLayout(layout)

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
        self.openGL_widget.camera_distance = distance
        self.scroll_zooming.setValue(int(distance))
        self.spinbox_zooming.setValue(float(distance))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
