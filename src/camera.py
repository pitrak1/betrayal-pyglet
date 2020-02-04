import pyglet
from pyglet.window import key
from pyglet.gl import *

class Camera():
    x, y, z = 0, 0, 0
    camera_left = 0
    camera_right = 800
    camera_bottom = 0
    camera_top = 600

    def __init__(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.camera_left, self.camera_right, self.camera_bottom, self.camera_top, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if button == 1:
            self.x -= dx*2
            self.y -= dy*2

    def on_mouse_scroll(self, x, y, dx, dy):
        pass
        # if dy > 0:
        #     self.camera_left -= 40
        #     self.camera_right += 40
        #     self.camera_bottom -= 30
        #     self.camera_top += 30
        # elif self.camera_right - self.camera_left > 500:
        #     self.camera_left += 40
        #     self.camera_right -= 40
        #     self.camera_bottom += 30
        #     self.camera_top -= 30

    def apply(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.camera_left, self.camera_right, self.camera_bottom, self.camera_top, -1, 1)
        glTranslatef(-self.x, -self.y, -self.z)
        glMatrixMode(GL_MODELVIEW)
