from sky_and_stars_imports import *
from OpenGL.GL import *
from OpenGL.GLU import *


class GLWidget(QGLWidget, MouseControllerWidget):
    def __init__(self, parent=None, scene=None):
        super(MouseControllerWidget, self).__init__(parent)
        super(GLWidget, self).__init__(parent)
        self.scene = scene
        self.camera_rotation_angle = 0.0 # радианы
        self.camera_lifting_angle = 0.0 # радианы
        self.camera_fov_angle = 60 # градусы
        self.camera_fov_angle_min = 5
        self.camera_fov_angle_max = 150
        self.camera_position = PointVector(0, 0, 0)
        self.frame_counter = 0

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0, 0, 0.05, 1.0)
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
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glPointSize(4.0)
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(
            self.get_camera_fov(), self.width() / self.height(), 0.1, 100.0
        )
        vector_view = self.get_view_vector()
        gluLookAt(
            self.camera_position.x,
            self.camera_position.y,
            self.camera_position.z,
            self.camera_position.x + vector_view.x,
            self.camera_position.y + vector_view.y,
            self.camera_position.z + vector_view.z,
            0, 0, 1
        )
        self.frame_counter += 1

        draw_coordinate_sphere_by_position(self.camera_position)
        for entity in self.scene.get_entities():
            entity.draw_shape()

        self.update()

    def contact_camera_fov(self):
        self.camera_fov_angle = max(
            self.camera_fov_angle_min, max(
                self.camera_fov_angle - self.get_wheel_rotation() // 8,
                self.camera_fov_angle_max
            )
        )

    def contact_camera_direction(self) -> None:
        m_move = self.get_mouse_move()
        self.camera_rotation_angle += m_move.x() * math.pi / 180
        self.camera_rotation_angle %= 2 * math.pi
        self.camera_lifting_angle = max(
            -math.pi, min(
                self.camera_lifting_angle + m_move.y() * math.pi / 180, math.pi
            )
        )
        QCursor.setPos(self._mouse_init_point)

    def get_camera_fov(self):
        self.contact_camera_fov()
        return self.camera_fov_angle

    def get_view_vector(self):
        self.contact_camera_direction()
        return self.view_vector

    @property
    def view_vector(self):
        return PointVector(
            math.cos(self.camera_rotation_angle) *
            math.cos(self.camera_lifting_angle),
            math.sin(self.camera_rotation_angle) *
            math.cos(self.camera_lifting_angle),
            math.sin(self.camera_lifting_angle)
        )

    def left_click_process(self, qpoint: QPoint):
        if qpoint is None:
            return
        if glReadPixels(qpoint.x(), qpoint.y(), 1, 1, GL_RGB, GL_UNSIGNED_BYTE) ==


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
