import pyglet
from src.shared import command, node

class State(node.Node):
	def __init__(self, asset_manager, set_state, add_command, testing):
		super().__init__()
		self.elements = {}
		self.asset_manager = asset_manager
		self.set_state = set_state
		self.add_command = add_command
		self.testing = testing

	def default_handler(self, command_, state=None):
		for element in self.elements.values():
			element.on_command(command_, self)

	def on_update(self, dt=None, state=None):
		for element in self.elements.values():
			element.on_update(dt, self)

	def draw(self):
		self.batch.draw()

	def trigger_translated_mouse_press(self, x, y, button, modifiers):
		self.add_command(command.Command(
			'client_translated_mouse_press', 
			{ 'x': x, 'y': y, 'button': button, 'modifiers': modifiers }
		))

	def trigger_translated_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.add_command(command.Command(
			'client_translated_mouse_drag', 
			{ 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'buttons': buttons, 'modifiers': modifiers }
		))
