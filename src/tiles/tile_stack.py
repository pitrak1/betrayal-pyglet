import random

class TileStack():
	def __init__(self, images):
		self.stack = []
		self.create_tiles(images)
		random.shuffle(self.stack)

	def create_tiles(self, images):
		raise NotImplementedError('__create_tiles must be overridden')

	def draw(self):
		return self.stack.pop(0)

	def get_by_name(self, name):
		tile = [x for x in self.stack if x.name == name]
		if len(tile):
			self.stack.remove(tile[0])
			return tile[0]