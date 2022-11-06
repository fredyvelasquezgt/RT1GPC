from libraryGame import Raytracer, V3, _color
from obj import Obj, Texture
from figures import Sphere, Material

width = 1024
height = 1024

snow = Material(diffuse=_color(235/255, 222/255, 203/255))
snow2 = Material(diffuse=_color(237/255, 223/255, 197/255))

algodon = Material(diffuse=_color(6/255, 6/255, 8/255))
nose = Material(diffuse=_color(242/255, 56/255, 39/255))
mouth = Material(diffuse=_color(90/255, 77/255, 69/255))
eye = Material(diffuse=_color(213/255, 192/255, 199/255))
light = Material(diffuse=_color(1, 1, 1))


rtx = Raytracer(width, height)
rtx.background = Texture('models/texture.bmp')

rtx.glClearBackground()
# Cuerpo
rtx.scene.append(Sphere(V3(0, -3, -10), 2, snow))
rtx.scene.append(Sphere(V3(0, 0, -15), 2.25, snow2))
rtx.scene.append(Sphere(V3(0, 2, -10), 1, snow))
# Elementos de la cara
rtx.scene.append(Sphere(V3(0.25, 0.80, -5), 0.05, mouth))
rtx.scene.append(Sphere(V3(-0.25, 0.80, -5), 0.05, mouth))
rtx.scene.append(Sphere(V3(0.10, 0.70, -5), 0.05, mouth))
rtx.scene.append(Sphere(V3(-0.10, 0.70, -5), 0.05, mouth))
# Nariz
rtx.scene.append(Sphere(V3(0, 1, -5), 0.15, nose))
# Ojos
rtx.scene.append(Sphere(V3(0.18, 1.18, -5), 0.08, eye))
rtx.scene.append(Sphere(V3(0.13, 0.95, -4), 0.04, algodon))
rtx.scene.append(Sphere(V3(-0.18, 1.19, -5), 0.08, eye))
rtx.scene.append(Sphere(V3(-0.15, 0.95, -4), 0.04, algodon))
# Reflejos
rtx.scene.append(Sphere(V3(0.12, 0.7, -3), 0.015, light))
rtx.scene.append(Sphere(V3(-0.10, 0.7, -3), 0.015, light))
# Botones
rtx.scene.append(Sphere(V3(0, -2.5, -8), 0.5, algodon))
rtx.scene.append(Sphere(V3(0, -1, -8), 0.35, algodon))
rtx.scene.append(Sphere(V3(0, 0.25, -8), 0.30, algodon))


rtx.glRender()


rtx.glFinish('output.bmp')
