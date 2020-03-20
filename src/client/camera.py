import pyglet
from pyglet.gl import *
from src.shared import constants, node
from src.client.states.game import game_state

class Camera(node.Node):
	def __init__(self):
		super().__init__()
		self.__x = constants.WINDOW_WIDTH // 4
		self.__y = constants.WINDOW_HEIGHT // 4
		self.__width = constants.WINDOW_WIDTH
		self.__height = constants.WINDOW_HEIGHT
		self.__zoom_factor = constants.CAMERA_STARTING_ZOOM_FACTOR
		self.__apply()

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glDepthFunc(GL_LEQUAL)

	def draw(self):
		self.__apply()

	def __apply(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		left = (self.__x) - (self.__width * self.__zoom_factor) // 2
		right = (self.__x) + (self.__width * self.__zoom_factor) // 2
		bottom = (self.__y) - (self.__height * self.__zoom_factor) // 2
		top = (self.__y) + (self.__height * self.__zoom_factor) // 2
		glOrtho(left, right, bottom, top, -1, 1)
		glTranslatef(-self.__x, -self.__y, 0)
		glMatrixMode(GL_MODELVIEW)

	def client_raw_mouse_press_handler(self, command, state):
		adjusted_x = self.__x * 2 + (command.data['x'] - self.__width // 2) * self.__zoom_factor
		adjusted_y = self.__y * 2 + (command.data['y'] - self.__height // 2) * self.__zoom_factor
		state.trigger_translated_mouse_press(adjusted_x, adjusted_y, command.data['button'], command.data['modifiers'])

	def client_raw_mouse_drag_handler(self, command, state):
		adjusted_x = self.__x * 2 + (command.data['x'] - self.__width // 2) * self.__zoom_factor
		adjusted_y = self.__y * 2 + (command.data['y'] - self.__height // 2) * self.__zoom_factor
		state.trigger_translated_mouse_drag(adjusted_x, adjusted_y, command.data['dx'], command.data['dy'], command.data['buttons'], command.data['modifiers'])

	def client_key_press_handler(self, command, state):
		if isinstance(state, game_state.GameState):
			if command.data['symbol'] == pyglet.window.key.W:
				self.__y += constants.CAMERA_PAN_COEFF * self.__zoom_factor
			elif command.data['symbol'] == pyglet.window.key.S:
				self.__y -= constants.CAMERA_PAN_COEFF * self.__zoom_factor
			elif command.data['symbol'] == pyglet.window.key.A:
				self.__x -= constants.CAMERA_PAN_COEFF * self.__zoom_factor
			elif command.data['symbol'] == pyglet.window.key.D:
				self.__x += constants.CAMERA_PAN_COEFF * self.__zoom_factor

	def client_mouse_scroll_handler(self, command, state):
		if isinstance(state, game_state.GameState):
			if command.data['dy'] > 0:
				if self.__zoom_factor < constants.CAMERA_MAX_ZOOM_FACTOR: 
					self.__zoom_factor *= 1 + constants.CAMERA_ZOOM_COEFF
			else:
				if self.__zoom_factor > constants.CAMERA_MIN_ZOOM_FACTOR: 
					self.__zoom_factor *= 1 - constants.CAMERA_ZOOM_COEFF


	

	
