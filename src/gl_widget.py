from sky_and_stars_imports import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np


class GLWidget(QGLWidget, MouseControllerWidget):
    def __init__(self, parent=None, scene=None):
        super(MouseControllerWidget, self).__init__(parent)
        super(GLWidget, self).__init__(parent)
        self.scene = scene
        self.parent = parent
        self.camera_rotation_angle = 0.0  # радианы
        self.camera_lifting_angle = 0.0  # радианы
        self.camera_fov_angle = 100.0  # градусы
        self.camera_fov_angle_min = 5
        self.camera_fov_angle_max = 120
        self.frame_counter = 0

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.05, 0, 0.1, 1.0)
        glEnable(GL_NORMALIZE)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
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
            0, 0, 0,
            vector_view.x, vector_view.y, vector_view.z,
            0, 0, 1
        )
        glMatrixMode(GL_MODELVIEW)
        self.frame_counter += 1

        draw_coordinate_sphere_by_position()
        for entity in self.scene.get_entities():
            entity.draw_shape()

        self.update()

    def contact_camera_fov(self):
        self.camera_fov_angle = max(
            self.camera_fov_angle_min,
            min(
                self.camera_fov_angle - self.get_wheel_rotation() / 120,
                self.camera_fov_angle_max
            )
        )
        self.parent.double_set_view_fov.setValue(self.camera_fov_angle)

    def contact_camera_direction(self) -> None:
        m_move = -self.get_mouse_move() * (
                self.get_camera_fov() / self.camera_fov_angle_max
        )
        self.camera_rotation_angle += m_move.x() * math.pi / 180
        self.camera_rotation_angle %= 2 * math.pi
        self.camera_lifting_angle = max(
            -math.pi / 2.00001,
            min(
                self.camera_lifting_angle + m_move.y() * math.pi / 180,
                math.pi / 2.00001
            )
        )
        self.parent.double_set_view_latitude.setValue(
            self.camera_lifting_angle * 180 / math.pi
        )
        self.parent.double_set_view_longitude.setValue(
            self.camera_rotation_angle * 180 / math.pi
        )

    def get_camera_fov(self):
        self.contact_camera_fov()
        return int(self.camera_fov_angle)

    def get_view_vector(self):
        self.contact_camera_direction()
        return self.view_vector

    @property
    def view_vector(self):
        return PointVector(
            math.cos(self.camera_rotation_angle) *
            math.cos(self.camera_lifting_angle) * 100,
            math.sin(self.camera_rotation_angle) *
            math.cos(self.camera_lifting_angle) * 100,
            math.sin(self.camera_lifting_angle) * 100,
        )

    def overrideable_left_click_process(self, qpoint: QPoint):
        if qpoint is None:
            return
        pixel_colors = sum(map(int, glReadPixels(
            qpoint.x(),
            self.height() - 1 - qpoint.y(),
            1, 1, GL_RGB, GL_UNSIGNED_BYTE
        )))
        if pixel_colors > 75:
            s, c = self.scene.set_active_star_and_constellation_nearest_to(
                self.get_vector_direction_by_click(qpoint)
            )
            self.parent.star_info_page.setPlainText(
                "\n".join(map(
                    lambda t: f"{t[0]}: {t[1]}",
                    list(s.reference.items()) + [
                        ("constellation", c.name if c else "None")
                    ]
                ))
            )

    def get_vector_direction_by_click(self, qpoint: QPoint) -> PointVector:
        gl_mv = glGetDoublev(GL_MODELVIEW_MATRIX)
        gl_proj = glGetDoublev(GL_PROJECTION_MATRIX)
        gl_vp = glGetIntegerv(GL_VIEWPORT)
        w_x = qpoint.x()
        w_y = self.height() - qpoint.y() - 1
        near_point = gluUnProject(w_x, w_y, 0.0, gl_mv, gl_proj, gl_vp)
        far_point = gluUnProject(w_x, w_y, 1.0, gl_mv, gl_proj, gl_vp)
        pv = PointVector(
            far_point[0] - near_point[0],
            far_point[1] - near_point[1],
            far_point[2] - near_point[2]
        )
        v = pv.np_vector
        v /= np.linalg.norm(v)
        return pv

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
