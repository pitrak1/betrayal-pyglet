from pyglet import window
from src.nodes import node
from src.tiles import tile, room_tile
from src.utils import grid_position
from src.states import selected_state as selected_state_module

class GridNode(node.Node):
	def __init__(self, grid_position, can_move):
		self.grid_position = grid_position
		self.can_move = can_move

	def mouse_press_handler(self, command, state):
		if state.__class__ == selected_state_module.SelectedState:
			if command.button == window.mouse.RIGHT and self.within_bounds(command.position) and self.can_move(state.selected.grid_position, self.grid_position):
				state.move_into_new_room(self.grid_position, state.selected.grid_position.grid_direction(self.grid_position))

	def within_bounds(self, position):
		return self.grid_position.within_square_bounds(position, grid_position.GRID_SIZE)

	def default_handler(self, command, state):
		pass

	def on_update(self, dt, state):
		pass
		
