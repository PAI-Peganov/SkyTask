import numpy as np

from src.simple_3d_editor_imports import *


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


def find_normal_figure2(figure, inner_point):
    points = [el.np_vector for el in figure.points]
    q = np.mean(points, axis=0)
    matrix = np.array([el - q for el in points])
    _, _, right_matrix = np.linalg.svd(matrix)
    if inner_point is None or np.dot(q - inner_point, right_matrix[2]) > 0:
        return right_matrix[2]
    return right_matrix[2] * (-1)


def out_light(func):
    def result(*args, **kwargs):
        glDisable(GL_LIGHTING)
        func(*args, **kwargs)
        glEnable(GL_LIGHTING)
    return result


def draw_point_param(point: list[float], radius: float, color: list[int]):
    glPushMatrix()
    glTranslate(point[0], point[1], point[2])
    set_material(color)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 8, 8)
    gluDeleteQuadric(quadric)
    glPopMatrix()


def draw_segment(figure: Segment, color=SEGMENT_COLOR):
    glBegin(GL_LINES)
    glColor3fv(color[:3])
    glVertex3fv(figure.point_a.np_vector)
    glVertex3fv(figure.point_b.np_vector)
    glEnd()


def draw_constellation(figure: Constellation):
    for el in figure.segments:
        draw_segment(el)


def draw_light(figure):
    glLightfv(figure.lightGL, GL_POSITION, [figure.x, figure.y, figure.z, 0.0])
