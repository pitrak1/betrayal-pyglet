from src.nodes import node

class VisibleNode(node.Node):
	def __init__(self, state_machine, tile, grid_x, grid_y):
		super().__init__(state_machine)
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.tile = tile
		self.tile.set_position(grid_x, grid_y)

	def on_draw(self):
		self.tile.on_draw(self.state_machine.is_selected(self))
