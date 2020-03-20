import pyglet
from src.client.states.menu import splash_state
from src.client import asset_manager, client, camera
from src.shared import threaded_queue, command, node
import threading

class Game():
	def __init__(self):
		self.__command_queue = threaded_queue.ThreadedQueue()
		self.__asset_manager = asset_manager.AssetManager()
		self.__camera = camera.Camera()
		self.__client = client.Client(self.__add_command)
		self.__current_state = splash_state.SplashState({ 'assets': self.__asset_manager }, self.__set_state, self.__add_command)

	def __set_state(self, state):
		self.__current_state = state

	def __add_command(self, command_):
		self.__command_queue.append(command_)

	def on_key_press(self, symbol, modifiers):
		self.__command_queue.append(command.Command('client_key_press', { 'symbol': symbol, 'modifiers': modifiers }))

	def on_text(self, text):
		self.__command_queue.append(command.Command('client_text_entered', { 'text': text }))

	def on_text_motion(self, motion):
		self.__command_queue.append(command.Command('client_text_motion', { 'motion': motion }))

	def on_text_motion_select(self, motion):
		self.__command_queue.append(command.Command('client_text_motion_select', { 'motion': motion }))

	def on_mouse_press(self, x, y, button, modifiers):
		self.__command_queue.append(command.Command(
			'client_raw_mouse_press', 
			{ 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }
		))

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.__command_queue.append(command.Command(
			'client_raw_mouse_drag', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'buttons': buttons, 'modifiers': modifiers }
		))

	def on_mouse_scroll(self, x, y, dx, dy):
		self.__command_queue.append(command.Command(
			'client_mouse_scroll', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy }
		))

	def on_update(self, dt):
		while self.__command_queue.has_elements():
			command_ = self.__command_queue.pop_front()
			print(f'popped {command_.type}')
			self.__camera.on_command(command_, self.__current_state)
			self.__client.on_command(command_, self.__current_state)
			self.__current_state.on_command(command_)

		self.__camera.on_update(dt, self.__current_state)
		self.__client.on_update(dt, self.__current_state)
		self.__current_state.on_update(dt)

	def draw(self):
		self.__camera.draw()
		self.__current_state.draw()
