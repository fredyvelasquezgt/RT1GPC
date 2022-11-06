from libraryGame import Renderer, V3
from obj import Texture
from shaders import *


width = 1920
height = 1080

rend = Renderer(width, height)

rend.directional_light = V3(1, 0, 0)

rend.active_texture = Texture('models/model.bmp')
rend.active_shader = holographic
rend.background = Texture('models/texture.bmp')
rend.glClearBackground()
rend.glLoadModel("models/model.obj",
                 translate=V3(-5, -2, -10),
                 scale=V3(2, 2, 2),
                 rotate=V3(0, 0, 0))
# rend.directional_light = V3(1, 1, 0)

rend.active_shader = colors


rend.glLoadModel("models/model.obj",
                 translate=V3(-5, 2, -10),
                 scale=V3(2, 2, 2),
                 rotate=V3(0, 0, 0))
rend.active_shader = toon

rend.glLoadModel("models/model.obj",
                 translate=V3(5, -2, -10),
                 scale=V3(2, 2, 2),
                 rotate=V3(0, 0, 0))

rend.active_shader = shader1

rend.glLoadModel("models/model.obj",
                 translate=V3(5, 2, -10),
                 scale=V3(2, 2, 2),
                 rotate=V3(0, 0, 0))

rend.glFinish("output.bmp")
