import pyglet
from pyglet.window import key
from pyglet.gl import *
from src.tiles import tile
from src.nodes import world_node

CAMERA_PAN_COEFF = 100

class Camera():
    def __init__(self, keys):
        self.x, self.y = world_node.MAP_WIDTH * tile.GRID_SIZE // 4, world_node.MAP_HEIGHT * tile.GRID_SIZE // 4
        self.width = 800
        self.height = 600
        self.zoom_factor = 1.0
        self.keys = keys
        self.apply()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthFunc(GL_LEQUAL)

    def translate_window_to_absolute_coordinates(self, x, y):
        adjusted_x = self.x * 2 + (x - self.width // 2) * self.zoom_factor
        adjusted_y = self.y * 2 + (y - self.height // 2) * self.zoom_factor
        return [adjusted_x, adjusted_y]

    def on_update(self, dt):
        if self.keys[key.W]:
            self.y += dt * CAMERA_PAN_COEFF * self.zoom_factor
        if self.keys[key.S]:
            self.y -= dt * CAMERA_PAN_COEFF * self.zoom_factor
        if self.keys[key.A]:
            self.x -= dt * CAMERA_PAN_COEFF * self.zoom_factor
        if self.keys[key.D]:
            self.x += dt * CAMERA_PAN_COEFF * self.zoom_factor

    def on_mouse_scroll(self, x, y, dx, dy):
        if dy > 0:
            if self.zoom_factor < 15: self.zoom_factor *= 1.1 
        else:
            if self.zoom_factor > 1: self.zoom_factor *= 0.9 

    def apply(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        left = (self.x) - (self.width * self.zoom_factor) // 2
        right = (self.x) + (self.width * self.zoom_factor) // 2
        bottom = (self.y) - (self.height * self.zoom_factor) // 2
        top = (self.y) + (self.height * self.zoom_factor) // 2
        glOrtho(left, right, bottom, top, -1, 1)
        glTranslatef(-self.x, -self.y, 0)
        glMatrixMode(GL_MODELVIEW)
