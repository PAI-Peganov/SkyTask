from src.sky_and_stars_imports import SEGMENT_COLOR
from src.basic_shapes import *
from src.point_vector import PointVector
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


def set_material(
    color, shininess=100.0, ambient=0.2, diffuse=0.9, specular=0.001
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


def draw_sphere_param(point: PointVector, radius: float, color: list[int]):
    #glPushMatrix()
    glTranslate(point[0], point[1], point[2])
    set_material(color)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 8, 8)
    gluDeleteQuadric(quadric)
    glTranslate(0, 0, 0)
    #glPopMatrix()


def draw_point_param(point: PointVector, radius: float, color: list[int]):
    glBegin(GL_POINTS)
    glPointSize(radius)
    glColor3fv(color)
    glVertex3f(point.x, point.y, point.z)
    glEnd()


def draw_segment(figure: Segment, color=SEGMENT_COLOR):
    glBegin(GL_LINES)
    glColor3fv(color[:3])
    glVertex3fv(figure.point_a.np_vector)
    glVertex3fv(figure.point_b.np_vector)
    glEnd()


def draw_constellation(figure: Constellation):
    for el in figure.segments:
        draw_segment(el)


def draw_coordinate_sphere_by_position(position: PointVector):
    glTranslatef(position.x, position.y, position.z)
    glLineWidth(1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glutWireSphere(5.0, 24, 18)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glTranslatef(0.0, 0.0, 0.0)


def draw_light(figure):
    glLightfv(figure.lightGL, GL_POSITION, [figure.x, figure.y, figure.z, 0.0])
