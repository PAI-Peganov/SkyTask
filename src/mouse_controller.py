from src.sky_and_stars_imports import *


class MouseControllerWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(QWidget, self).__init__(parent)
        self.setMouseTracking(True)
        self._mouse_move = None
        self._mouse_init_point = None
        self._wheel_rotation = 0

    def get_wheel_rotation(self):
        w_r = self._wheel_rotation
        self._wheel_rotation = 0
        return w_r

    def get_mouse_move(self) -> QPoint:
        if self._mouse_move is None:
            return QPoint(0, 0)
        m_move = self._mouse_move
        self._mouse_move = None
        return m_move

    def try_get_mouse_position_inside(self) -> QPoint | None:
        m_pos = self.mapFromGlobal(QCursor.pos())
        if 0 <= m_pos.x() < self.size().width():
            if 0 <= m_pos.y() < self.size().height():
                return m_pos
        return None

    def left_click_process(self, qpoint: QPoint):
        pass

    def mousePressEvent(self, event):
        if event == Qt.MouseButton.RightButton:
            self._mouse_init_point = self.try_get_mouse_position_inside()
        if event == Qt.MouseButton.LeftButton:
            self.left_click_process(
                self.try_get_mouse_position_inside()
            )

    def mouseMoveEvent(self, event):
        if self._mouse_init_point:
            self._mouse_move = event.pos() - self._mouse_init_point
            QCursor.setPos(self._mouse_init_point)

    def mouseReleaseEvent(self, event):
        if event == Qt.MouseButton.RightButton:
            self._mouse_init_point = None

    def wheelEvent(self, event):
        self._wheel_rotation = event.pixelDelta().y()
