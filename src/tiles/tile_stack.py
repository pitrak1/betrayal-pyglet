import random
from src import node as node_module

class TileStack(node_module.Node):
	def __init__(self, images, misc):
		self.stack = []
		self.create_tiles(images, misc)
		random.shuffle(self.stack)

	def create_tiles(self, images, misc):
		raise NotImplementedError('create_tiles must be overridden')

	def draw(self):
		return self.stack.pop(0)

	def get_by_name(self, name):
		tile = [x for x in self.stack if x.name == name]
		if not len(tile): raise Exception('get_by_name failed because element by name was not in stack')
		self.stack.remove(tile[0])
		return tile[0]

	def on_draw(self, state):
		pass

	def default_handler(self, command, state):
		pass

	def on_update(self, dt, state):
		pass