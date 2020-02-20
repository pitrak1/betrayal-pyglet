from src.nodes import node
from src.states import selected_state as selected_state_module

class VisibleNode(node.Node):
	def __init__(self, tile, grid_position):
		self.grid_position = grid_position
		self.tile = tile
		self.tile.set_position(grid_position)

	def on_draw(self, state):
		if state.__class__ == selected_state_module.SelectedState:
			self.tile.on_draw(state.is_selected(self))
		else:
			self.tile.on_draw(False)
