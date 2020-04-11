import pyglet
from src.client.menu import splash_state
from src.client import asset_manager, client
from src.shared import threaded_queue, command, node, logger

class Game():
	def __init__(self, testing=False):
		self.command_queue = threaded_queue.ThreadedQueue()
		self.asset_manager = asset_manager.AssetManager()
		self.client = client.Client(self.add_command, testing=testing)
		self.current_state = splash_state.SplashState(self.asset_manager, self.set_state, self.add_command, testing=testing)

	def set_state(self, state):
		self.current_state = state

	def add_command(self, command_):
		logger.log(f'Adding command {command_.type} ', logger.LOG_LEVEL_COMMAND, data=command_.data)
		self.command_queue.append(command_)

	def on_key_press(self, symbol, modifiers):
		self.add_command(command.Command('client_key_press', { 'symbol': symbol, 'modifiers': modifiers }))

	def on_text(self, text):
		self.add_command(command.Command('client_text_entered', { 'text': text }))

	def on_text_motion(self, motion):
		self.add_command(command.Command('client_text_motion', { 'motion': motion }))

	def on_text_motion_select(self, motion):
		self.add_command(command.Command('client_text_motion_select', { 'motion': motion }))

	def on_mouse_press(self, x, y, button, modifiers):
		self.add_command(command.Command(
			'client_mouse_press', 
			{ 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }
		))

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.add_command(command.Command(
			'client_mouse_drag', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'buttons': buttons, 'modifiers': modifiers }
		))

	def on_mouse_scroll(self, x, y, dx, dy):
		self.add_command(command.Command(
			'client_mouse_scroll', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy }
		))

	def on_update(self, dt):
		while self.command_queue.has_elements():
			command_ = self.command_queue.pop_front()
			logger.log(f'Handling command {command_.type} ', logger.LOG_LEVEL_COMMAND, data=command_.data)
			self.client.on_command(command_, self.current_state)
			self.current_state.on_command(command_)

		self.client.on_update(dt, self.current_state)
		self.current_state.on_update(dt)

	def draw(self):
		self.current_state.draw()
