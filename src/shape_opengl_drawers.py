from src.sky_and_stars_imports import SEGMENT_COLOR
from src.base_entities import *
from src.point_vector import PointVector
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


def set_material(
    color: list[float], shininess: float = 100.0, ambient: float = 0.2,
    diffuse: float = 0.9, specular: float = 0.001
):
    color = np.array(color)
    ambient_val = color * ambient
    ambient_val[3] = color[3]
    diffuse_val = color * diffuse
    diffuse_val[3] = color[3]
    specular_val = np.ones(shape=(4,), dtype=float) * specular
    specular_val[3] = color[3]
    # Настройка материала
    glEnable(GL_LIGHTING)
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_val)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_val)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_val)
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess)


def out_light(func):
    def result(*args, **kwargs):
        glDisable(GL_LIGHTING)
        func(*args, **kwargs)
        glEnable(GL_LIGHTING)
    return result


def draw_point_param(point: np.array, radius: float, color: list[float]):
    glPointSize(radius)
    glColor3fv(color[:3])
    glBegin(GL_POINTS)
    glVertex3f(*point)
    glEnd()


def draw_segment(figure: Segment, color: list[float] = SEGMENT_COLOR):
    glBegin(GL_LINES)
    glColor3fv(color[:3])
    glVertex3fv(figure.point_a.np_vector)
    glVertex3fv(figure.point_b.np_vector)
    glEnd()


def draw_polyline(star_points: list[Star], color: list[float] = SEGMENT_COLOR):
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3fv(color[:3])
    for el in star_points:
        glVertex3fv(el.get_position_numpy())
    glEnd()


def draw_coordinate_sphere_by_position():
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glColor3f(0.1, 0.1, 0.1)
    glLineWidth(0.1)
    quadric = gluNewQuadric()
    gluSphere(quadric, 55.0, 24, 18)  # случайный радиус, 24 часа, 180 градусов / 10
    gluDeleteQuadric(quadric)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


def draw_light(figure):
    glLightfv(figure.lightGL, GL_POSITION, [figure.x, figure.y, figure.z, 0.0])
