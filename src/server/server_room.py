from src.shared import node as node_module

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class ServerRoom(node_module.Node):
	def __init__(self, entry):
		super().__init__()
		for key, value in entry.items():
			setattr(self, key, value)

		self.players = []
		self.links = []

	def set_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y
