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


def draw_sphere(point: list[float], radius: float, color: list[int]):
    glPushMatrix()
    glTranslate(point[0], point[1], point[2])
    set_material(color)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 8, 8)
    gluDeleteQuadric(quadric)
    glPopMatrix()


@out_light
def draw_point(figure):
    glBegin(GL_POINTS)
    glColor3fv(POINT_COLOR[:3])
    glVertex3f(figure.x, figure.y, figure.z)
    glEnd()


@out_light
def draw_segment(figure, color=SEGMENT_COLOR):
    glBegin(GL_LINES)
    glColor3fv(color[:3])
    glVertex3fv(figure.point_a.np_vector)
    glVertex3fv(figure.point_b.np_vector)
    glEnd()


@out_light
def draw_contur2(points, color=SEGMENT_COLOR):
    glBegin(GL_LINE_LOOP)
    glColor3fv(color[:3])
    for point in points:
        glVertex3fv(point.np_vector)
    glEnd()


def draw_figure2(figure, inner_point=None):
    set_material(FIGURE2_COLOR)
    first_point = figure.points[0].np_vector
    normal_vec = find_normal_figure2(figure, inner_point)
    for i in range(2, len(figure.points)):
        glBegin(GL_POLYGON)
        glNormal3fv(normal_vec)
        glVertex3fv(first_point)
        glVertex3fv(figure.points[i - 1].np_vector)
        glVertex3fv(figure.points[i].np_vector)
        glEnd()
    draw_contur2(figure.points, color=EDGE_COLOR)


def draw_plane(figure):
    set_material(PLANE_COLOR)
    glBegin(GL_POLYGON)
    glNormal3fv(figure.normal)
    if len(figure.contur) > 0:
        for segment in figure.contur[0].segments:
            glVertex3fv(segment.point_a.np_vector)
        glEnd()
        draw_contur2([el.point_a for el in figure.contur[0].segments])
    else:
        # не забыть: size меньше 2000,
        size = 1000
        glVertex3f(size, size, figure.count_new_z(size, size))
        glVertex3f(size, -size, figure.count_new_z(size, -size))
        glVertex3f(-size, -size, figure.count_new_z(-size, -size))
        glVertex3f(-size, size, figure.count_new_z(-size, size))
        glEnd()


def draw_figure3(figure):
    for face in figure.faces:
        draw_figure2(face, figure.get_center())


def draw_light(figure):
    glLightfv(figure.lightGL, GL_POSITION, [figure.x, figure.y, figure.z, 0.0])
