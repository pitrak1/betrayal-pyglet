import pyglet
from src.common import command, node

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
