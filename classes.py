import os
import platform
import numpy as np
import math


class Object3d:
    def __init__(self, model, position, rotation):
        self.position = np.array(position, dtype=float)
        self.rotation = np.array(rotation, dtype=float)
        self.model, self.edges = self.obj_to_model(model)

    def obj_to_model(self, file):
        f = open(file, "r")
        model = []
        edges = []
        for line in f:
            if line.startswith("v "):
                line = line.replace("v ", "").strip().split(" ")
                model.append(np.array([float(line[0]), float(line[1]), float(line[2].strip())]))
            elif line.startswith("f "):
                line = line.replace("f ", "").strip().split(" ")
                edge = [int(x.split("/")[0]) - 1 for x in line]
                edges.append(edge)

        return model, edges

    def points(self):
        x_axis = [1, 0, 0]

        mod = []
        for point in self.model:
            p = self.rotation_matrix(x_axis, self.rotation[0]).dot(point)
            mod.append(p)

        return mod + self.position

    def rotation_matrix(self, axis, theta):
        axis = np.asarray(axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array(
            [
                [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc],
            ]
        )


class Camera3d:
    def __init__(self, alpha, beta, near, far):
        self.alpha = alpha
        self.beta = beta
        self.near = near
        self.far = far

    def calculate_transform_matrix(self):
        return np.array(
            [
                [math.tan(self.alpha), 0, 0, 0],
                [0, math.tan(self.beta), 0, 0],
                [
                    0,
                    0,
                    (self.far + self.near) / (self.far - self.near),
                    (2 * self.near * self.far) / (self.far - self.near),
                ],
                [0, 0, -1, 0],
            ]
        )

    def calculate_x_y(self, position):
        position = np.append(position, position[-1])
        transformed_position = position.dot(self.calculate_transform_matrix())
        transformed_position /= transformed_position[-1]
        return transformed_position[0], transformed_position[1]


class RenderEngine:
    def __init__(self, room_height, room_width):
        self.room_height = room_height
        self.room_width = room_width
        self.room = []

        self.fill_room()

    def clear(self):
        self.fill_room()
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")

    def fill_room(self):
        self.room.clear()
        for _ in range(0, self.room_height):
            r = []
            for _ in range(0, self.room_width):
                r.append(" ")
            self.room.append(r)

    def print_room(self):
        for i in self.room:
            toPrint = ""
            for j in i:
                toPrint += j
            print(toPrint)

    def normalize(self, i, j):
        if i < -1 or j < -1:
            return -1, -1
        if i > 1 or j > 1:
            return -1, -1

        i = int(((i + 1) / 2) * self.room_height)
        j = int(((j + 1) / 2) * self.room_width)
        return i, j

    def draw_point(self, i, j):
        if i < 0:
            return
        if j < 0:
            return
        if i >= self.room_height:
            return
        if j >= self.room_width:
            return

        self.room[i][j] = "X"

    def draw_line(self, i, j, x, y):
        if i == -1 or j == -1 or x == -1 or y == -1:
            return

        lerp = lambda start, end, t: start + t * (end - start)
        distance = lambda x, y: math.sqrt(x ** 2 + y ** 2)

        iterations = int(distance(i - x, j - y))
        for k in range(iterations):
            t = k / iterations
            ax = int(lerp(i, x, t))
            ay = int(lerp(j, y, t))
            self.draw_point(ax, ay)

    def draw_rectangle(self, x, y, width, height):
        for j in range(x, x + width):
            for i in range(y, y + height):
                self.draw_point(i, j)
