import pyglet
from pyglet.gl import *
from src.shared import constants, node
from src.client.states.game import game_state as game_state_module

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

	def client_raw_mouse_drag_handler(self, command, state):
		adjusted_x = self.x * 2 + (command.data['x'] - self.width // 2) * self.zoom_factor
		adjusted_y = self.y * 2 + (command.data['y'] - self.height // 2) * self.zoom_factor
		state.trigger_translated_mouse_drag(adjusted_x, adjusted_y, command.data['dx'], command.data['dy'], command.data['buttons'], command.data['modifiers'])

	def client_key_press_handler(self, command, state):
		if isinstance(state, game_state_module.GameState):
			if command.data['symbol'] == pyglet.window.key.W:
				self.y += constants.CAMERA_PAN_COEFF * self.zoom_factor
			elif command.data['symbol'] == pyglet.window.key.S:
				self.y -= constants.CAMERA_PAN_COEFF * self.zoom_factor
			elif command.data['symbol'] == pyglet.window.key.A:
				self.x -= constants.CAMERA_PAN_COEFF * self.zoom_factor
			elif command.data['symbol'] == pyglet.window.key.D:
				self.x += constants.CAMERA_PAN_COEFF * self.zoom_factor

	def client_mouse_scroll_handler(self, command, state):
		if isinstance(state, game_state_module.GameState):
			if command.data['dy'] > 0:
				if self.zoom_factor < constants.CAMERA_MAX_ZOOM_FACTOR: 
					self.zoom_factor *= 1 + constants.CAMERA_ZOOM_COEFF
			else:
				if self.zoom_factor > constants.CAMERA_MIN_ZOOM_FACTOR: 
					self.zoom_factor *= 1 - constants.CAMERA_ZOOM_COEFF


	

	
