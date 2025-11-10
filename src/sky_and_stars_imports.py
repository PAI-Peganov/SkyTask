#!/usr/bin/env python3

import sys
import os
import traceback
from collections import deque, defaultdict
import math
import zipfile
import datetime
from pathlib import Path

ERROR_EXCEPTION = 1
ERROR_WRONG_SETTINGS = 2
ERROR_PYTHON_VERSION = 3
ERROR_MODULES_MISSING = 4
ERROR_QT_VERSION = 5
ERROR_OPENGL_VERSION = 6
ERROR_NUMPY_VERSION = 6

SEGMENT_COLOR = [0.0, 0.9, 0.6, 1.0]
POINT_COLOR = [1.0, 0.0, 0.0, 1.0]

if sys.version_info < (3, 10):
    print('Use python >= 3.10', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

sys.excepthook = lambda x, y, z: (
    print("".join(traceback.format_exception(x, y, z)))
)

try:
    from PyQt5 import QtGui, QtCore, QtWidgets, QtOpenGL, uic
    from PyQt5.QtGui import QCursor, QWheelEvent
    from PyQt5.QtCore import QEvent, Qt, QPoint
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                                 QWidget, QDialog, QLabel, QLineEdit,
                                 QPushButton, QMessageBox, QFormLayout,
                                 QDoubleSpinBox, QSpinBox, QHBoxLayout,
                                 QTreeWidgetItem)
    from PyQt5.QtOpenGL import QGLWidget
except Exception as e:
    print('PyQt5 not found: "{}".'.format(e),
          file=sys.stderr)
    sys.exit(ERROR_QT_VERSION)

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except Exception as e:
    print('OpenGL not found: "{}".'.format(e),
          file=sys.stderr)
    sys.exit(ERROR_OPENGL_VERSION)

try:
    import numpy as np
    from PIL import Image
except Exception as e:
    print('Not found: "{}".'.format(e),
          file=sys.stderr)
    sys.exit(ERROR_NUMPY_VERSION)

try:
    from src.mouse_controller import *
    from src.star_parser import *
    from src.point_vector import *
    from src.shape_opengl_drawers import *
    from src.basic_shapes import *
    from src.scene_base import *
    from src.adding_windows import *
    from src.qt_app import *
except Exception as e:
    print('App modules not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)
