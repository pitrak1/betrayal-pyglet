import pyglet
from src.client.states.menu import splash_state
from src.client import asset_manager, client, camera
from src.shared import threaded_queue, command, node
import threading

class Game():
	def __init__(self):
		self.command_queue = threaded_queue.ThreadedQueue()
		self.asset_manager = asset_manager.AssetManager()
		self.camera = camera.Camera()
		self.client = client.Client(self.add_command)
		self.current_state = splash_state.SplashState(self.asset_manager, self.set_state, self.add_command)

	def set_state(self, state):
		self.current_state = state

	def add_command(self, command_):
		self.command_queue.append(command_)

	def on_key_press(self, symbol, modifiers):
		self.command_queue.append(command.Command('client_key_press', { 'symbol': symbol, 'modifiers': modifiers }))

	def on_text(self, text):
		self.command_queue.append(command.Command('client_text_entered', { 'text': text }))

	def on_text_motion(self, motion):
		self.command_queue.append(command.Command('client_text_motion', { 'motion': motion }))

	def on_text_motion_select(self, motion):
		self.command_queue.append(command.Command('client_text_motion_select', { 'motion': motion }))

	def on_mouse_press(self, x, y, button, modifiers):
		self.command_queue.append(command.Command(
			'client_raw_mouse_press', 
			{ 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }
		))

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.command_queue.append(command.Command(
			'client_raw_mouse_drag', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'buttons': buttons, 'modifiers': modifiers }
		))

	def on_mouse_scroll(self, x, y, dx, dy):
		self.command_queue.append(command.Command(
			'client_mouse_scroll', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy }
		))

	def on_update(self, dt):
		while self.command_queue.has_elements():
			command_ = self.command_queue.pop_front()
			print(f'popped {command_.type}')
			self.camera.on_command(command_, self.current_state)
			self.client.on_command(command_, self.current_state)
			self.current_state.on_command(command_)

		self.camera.on_update(dt, self.current_state)
		self.client.on_update(dt, self.current_state)
		self.current_state.on_update(dt)

	def draw(self):
		self.camera.draw()
		self.current_state.draw()
