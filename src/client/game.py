import pyglet
from src.client.states.menu import splash_state
from src.client import asset_manager, client as client_module, camera as camera_module
from src.shared import threaded_queue, command as command_module, node
import threading

class Game():
	def __init__(self):
		self.command_queue = threaded_queue.ThreadedQueue()
		self.asset_manager = asset_manager.AssetManager()

		self.camera = camera_module.Camera()
		self.client = client_module.Client(self.add_command)
		data = { 'assets': self.asset_manager }
		self.current_state = splash_state.SplashState(data, self.set_state, self.add_command)

	def set_state(self, state):
		self.current_state = state

	def add_command(self, c):
		self.command_queue.append(c)

	def on_key_press(self, symbol, modifiers):
		self.command_queue.append(command_module.Command('client_key_press', { 'symbol': symbol, 'modifiers': modifiers }))

	def on_text(self, text):
		self.command_queue.append(command_module.Command('client_text_entered', { 'text': text }))

	def on_mouse_press(self, x, y, button, modifiers):
		self.command_queue.append(command_module.Command(
			'client_raw_mouse_press', 
			{ 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }
		))

	def on_mouse_scroll(self, x, y, dx, dy):
		self.command_queue.append(command_module.Command(
			'client_mouse_scroll', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy }
		))

	def on_update(self, dt):
		while self.command_queue.has_elements():
			command = self.command_queue.pop_front()
			print(f'popped {command.type}')
			self.camera.on_command(command, self.current_state)
			self.client.on_command(command, self.current_state)
			self.current_state.on_command(command)

		self.camera.on_update(dt, self.current_state)
		self.client.on_update(dt, self.current_state)
		self.current_state.on_update(dt)

	def draw(self):
		self.camera.draw()
		self.current_state.draw()
