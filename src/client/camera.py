import pyglet
from pyglet.gl import *
from src.shared import constants, node
# from src.client.states.menu import menu_state

class Camera(node.Node):
	def __init__(self):
		super().__init__()
		self.x = constants.WINDOW_WIDTH // 4
		self.y = constants.WINDOW_HEIGHT // 4
		self.width = constants.WINDOW_WIDTH
		self.height = constants.WINDOW_HEIGHT
		self.zoom_factor = constants.CAMERA_STARTING_ZOOM_FACTOR
		self.__apply()

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glDepthFunc(GL_LEQUAL)

	def draw(self):
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

	def client_raw_mouse_press_handler(self, command, state):
		adjusted_x = self.x * 2 + (command.data['x'] - self.width // 2) * self.zoom_factor
		adjusted_y = self.y * 2 + (command.data['y'] - self.height // 2) * self.zoom_factor
		state.trigger_translated_mouse_press(adjusted_x, adjusted_y, command.data['button'], command.data['modifiers'])

	# def key_press_handler(self, command, state):
	# 	if not isinstance(state, menu_state.MenuState):
	# 		if command.symbol == pyglet.window.key.W:
	# 			self.y += constants.CAMERA_PAN_COEFF * self.zoom_factor
	# 		elif command.symbol == pyglet.window.key.S:
	# 			self.y -= constants.CAMERA_PAN_COEFF * self.zoom_factor
	# 		elif command.symbol == pyglet.window.key.A:
	# 			self.x -= constants.CAMERA_PAN_COEFF * self.zoom_factor
	# 		elif command.symbol == pyglet.window.key.D:
	# 			self.x += constants.CAMERA_PAN_COEFF * self.zoom_factor

	# def mouse_scroll_handler(self, command, state):
	# 	if not isinstance(state, menu_state.MenuState):
	# 		if command.dy > 0:
	# 			if self.zoom_factor < constants.CAMERA_MAX_ZOOM_FACTOR: 
	# 				self.zoom_factor *= 1 + constants.CAMERA_ZOOM_COEFF
	# 		else:
	# 			if self.zoom_factor > constants.CAMERA_MIN_ZOOM_FACTOR: 
	# 				self.zoom_factor *= 1 - constants.CAMERA_ZOOM_COEFF


	

	
