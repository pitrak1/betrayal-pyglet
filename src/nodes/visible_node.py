from src.nodes import node

class VisibleNode(node.Node):
	def __init__(self, state_machine, tile, grid_position):
		super().__init__(state_machine)
		self.grid_position = grid_position
		self.tile = tile
		self.tile.set_position(grid_position)

	def on_draw(self):
		self.tile.on_draw(self.state_machine.is_selected(self))
