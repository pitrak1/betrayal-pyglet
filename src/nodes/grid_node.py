from pyglet import window
from src.nodes import node
from src.tiles import tile, room_tile
from src.utils import grid_position

class GridNode(node.Node):
	def __init__(self, state_machine, grid_position, world):
		super().__init__(state_machine)
		self.grid_position = grid_position
		self.world = world

	def mouse_press_handler(self, command):
		if self.state_machine.current_state.__class__.__name__ != 'RotatingRoomState' and self.within_bounds(command.position):
			if command.button == window.mouse.RIGHT:
				if self.state_machine.current_state.__class__.__name__ == 'SelectedState' and self.world.can_move(self.state_machine.current_state.selected.grid_position, self.grid_position):
					character = self.state_machine.current_state.selected
					self.state_machine.rotate_room(self.grid_position, self.state_machine.current_state.selected.grid_position.grid_direction(self.grid_position))
					self.state_machine.move(self.grid_position, character=character)

	def within_bounds(self, position):
		return self.grid_position.within_square_bounds(position, grid_position.GRID_SIZE)

	def default_handler(self, command):
		pass

	def on_update(self, dt):
		pass
		
