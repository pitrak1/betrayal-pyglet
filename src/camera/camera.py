import pyglet
from pyglet.window import key
from pyglet.gl import *
from src.tiles import tile
from src import node as node_module
from src.utils import constants
from src.states import commands as commands_module

class Camera(node_module.Node):
	def __init__(self):
		self.x = constants.GRID_WIDTH * constants.GRID_SIZE // 4
		self.y = constants.GRID_HEIGHT * constants.GRID_SIZE // 4
		self.width = constants.WINDOW_WIDTH
		self.height = constants.WINDOW_HEIGHT
		self.zoom_factor = constants.CAMERA_STARTING_ZOOM_FACTOR
		self.__apply()

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glDepthFunc(GL_LEQUAL)

	def on_update(self, dt, state, keys):
		if keys[key.W]:
			self.y += dt * constants.CAMERA_PAN_COEFF * self.zoom_factor
		if keys[key.S]:
			self.y -= dt * constants.CAMERA_PAN_COEFF * self.zoom_factor
		if keys[key.A]:
			self.x -= dt * constants.CAMERA_PAN_COEFF * self.zoom_factor
		if keys[key.D]:
			self.x += dt * constants.CAMERA_PAN_COEFF * self.zoom_factor

	def raw_mouse_press_handler(self, command, state):
		adjusted_x = self.x * 2 + (command.x - self.width // 2) * self.zoom_factor
		adjusted_y = self.y * 2 + (command.y - self.height // 2) * self.zoom_factor
		state.trigger_translated_mouse_press(adjusted_x, adjusted_y, command.button, command.modifiers)

	def mouse_scroll_handler(self, command, state):
		if command.dy > 0:
			if self.zoom_factor < constants.CAMERA_MAX_ZOOM_FACTOR: 
				self.zoom_factor *= 1 + constants.CAMERA_ZOOM_COEFF
		else:
			if self.zoom_factor > constants.CAMERA_MIN_ZOOM_FACTOR: 
				self.zoom_factor *= 1 - constants.CAMERA_ZOOM_COEFF

	def default_handler(self, command, state):
		pass

	def on_draw(self, state):
		self.__apply()

	def __apply(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		left = (self.x) - (self.width * self.zoom_factor) // 2
		right = (self.x) + (self.width * self.zoom_factor) // 2
		bottom = (self.y) - (self.height * self.zoom_factor) // 2
		top = (self.y) + (self.height * self.zoom_factor) // 2
		glOrtho(left, right, bottom, top, -1, 1)
		glTranslatef(-self.x, -self.y, 0)
		glMatrixMode(GL_MODELVIEW)
