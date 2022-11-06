import struct
from collections import namedtuple

from obj import Obj


from numpy import sin, cos, tan


from myLibrary import *

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def _color(r, g, b):
    # Acepta valores de 0 a 1
    # Se asegura que la información de color se guarda solamente en 3 bytes
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


def baryCoords(A, B, C, P):
    # u es para A, v es para B, w es para C
    try:
        # PCB/ABC
        u = (((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) /
             ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        # PCA/ABC
        v = (((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) /
             ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w


BLACK = _color(0, 0, 0)
WHITE = _color(1, 1, 1)


class Raytracer(object):
    def __init__(self, width, height):
        # Constructor
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.camPosition = V3(0, 0, 0)
        self.fov = 60

        self.glCreateWindow(width, height)

        self.background = None
        self.scene = []

    def glFinish(self, filename):
        # Crea un archivo BMP y lo llena con la información dentro de self.pixels
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = int(width)
        self.vpHeight = int(height)

    def glClearColor(self, r, g, b):
        self.clear_color = _color(r, g, b)

    def glClear(self):
        # Crea una lista 2D de pixeles y a cada valor le asigna 3 bytes de color
        self.pixels = [[self.clear_color for y in range(self.height)]
                       for x in range(self.width)]

        # self.zbuffer = [[float('inf')for y in range(self.height)]
        #                 for x in range(self.width)]

    def glViewportClear(self, color=None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x, y, color)

    def glColor(self, r, g, b):
        self.curr_color = _color(r, g, b)

    def glPoint(self, x, y, color=None):
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color

    def glPoint_NDC(self, x, y, color=None):
        x = int((x + 1) * (self.vpWidth / 2) + self.vpX)
        y = int((y + 1) * (self.vpHeight / 2) + self.vpY)

        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color

    def glLine(self, v0, v1, color=None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y1, color)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glLine_NDC(self, v0, v1, color=None):

        x0 = int((v0.x + 1) * (self.vpWidth / 2) + self.vpX)
        x1 = int((v1.x + 1) * (self.vpWidth / 2) + self.vpX)
        y0 = int((v0.y + 1) * (self.vpHeight / 2) + self.vpY)
        y1 = int((v1.y + 1) * (self.vpHeight / 2) + self.vpY)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glTriangle_standard(self, A, B, C, color=None):

        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        def flatBottomTriangle(v1, v2, v3):
            try:
                d_21 = (v2.x - v1.x) / (v2.y - v1.y)
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
            except:
                pass
            else:
                x1 = v2.x
                x2 = v3.x
                for y in range(v2.y, v1.y + 1):
                    self.glLine(V2(int(x1), y), V2(int(x2), y), color)
                    x1 += d_21
                    x2 += d_31

        def flatTopTriangle(v1, v2, v3):
            try:
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
                d_32 = (v3.x - v2.x) / (v3.y - v2.y)
            except:
                pass
            else:
                x1 = v3.x
                x2 = v3.x

                for y in range(v3.y, v1.y + 1):
                    self.glLine(V2(int(x1), y), V2(int(x2), y), color)
                    x1 += d_31
                    x2 += d_32

        if B.y == C.y:
            # triangulo con base inferior plana
            flatBottomTriangle(A, B, C)
        elif A.y == B.y:
            # triangulo con base superior plana
            flatTopTriangle(A, B, C)
        else:
            # dividir el triangulo en dos
            # dibujar ambos casos
            # Teorema de intercepto
            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottomTriangle(A, B, D)
            flatTopTriangle(B, D, C)

    def glTriangle_bc(self, A, B, C, texCoords=(), normals=(), verts=(),  color=None):
        # Bounding Box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        triangleNormal = crossProduct(subtract(
            verts[1], verts[0]), subtract(verts[2], verts[0]))
        triangleNormal = normalize(triangleNormal)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A.z * u + B.z * v + C.z * w

                    if 0 <= x < self.width and 0 <= y < self.height:
                        if z < self.zbuffer[x][y] and z <= 1 and z >= -1:

                            self.zbuffer[x][y] = z

                            if self.active_shader:

                                r, g, b = self.active_shader(self,
                                                             verts=verts,
                                                             baryCoords=(
                                                                 u, v, w),
                                                             texCoords=texCoords,
                                                             normals=normals,
                                                             triangleNormal=triangleNormal,
                                                             color=color or self.curr_color)

                                self.glPoint(x, y, _color(r, g, b))

                            else:
                                self.glPoint(x, y, color or self.curr_color)

    def glClearBackground(self):
        if self.background:
            for x in range(self.vpX, self.vpX + self.vpWidth):
                for y in range(self.vpY, self.vpY + self.vpHeight):

                    tx = (x - self.vpX) / self.vpWidth
                    ty = (y - self.vpY) / self.vpHeight

                    self.glPoint(x, y, self.background.getColor(tx, ty))

    def glRender(self):

        for y in range(self.height):
            for x in range(self.width):
                Px = 2*((x+0.5)/self.width)-1
                Py = 2*((y+0.5)/self.height)-1
                t = tan((self.fov * pi() / 180) / 2)
                r = t * self.width/self.height
                Px *= r
                Py *= t

                direction = V3(Px, Py, -1)
                direction = normalize(direction)
                self.glPoint(x, y, self.cast_ray(self.camPosition, direction))

    def cast_ray(self, orig, dir):
        material = self.scene_intersect(orig, dir)

        if material == None:
            return self.clear_color
        else:
            return material.diffuse

    def scene_intersect(self, orig, dir):
        depth = float('inf')
        material = None

        for obj in self.scene:
            intersect = obj.ray_intersect(orig, dir)
            if intersect != None:
                if intersect.distance < depth:
                    depth = intersect.distance
                    material = obj.material

        return material
