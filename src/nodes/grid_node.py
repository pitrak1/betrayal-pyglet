from pyglet import window
from src.nodes import node
from src.tiles import tile, room_tile

class GridNode(node.Node):
	def __init__(self, state_machine, grid_x, grid_y, world):
		super().__init__(state_machine)
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.world = world

	def mouse_press_handler(self, command):
		if self.state_machine.current_state.__class__.__name__ != 'RotatingRoomState' and self.within_bounds(command.x, command.y):
			if command.button == window.mouse.RIGHT:
				if self.state_machine.current_state.__class__.__name__ == 'SelectedState' and self.world.can_move(self.state_machine.current_state.selected.grid_x, self.state_machine.current_state.selected.grid_y, self.grid_x, self.grid_y):
					character = self.state_machine.current_state.selected
					self.state_machine.rotate_room(self.grid_x, self.grid_y, self.world.move_direction(self.state_machine.current_state.selected.grid_x, self.state_machine.current_state.selected.grid_y, self.grid_x, self.grid_y))
					self.state_machine.move(self.grid_x, self.grid_y, character=character)

	def within_bounds(self, x, y):
		node_x = tile.GRID_SIZE * self.grid_x
		node_y = tile.GRID_SIZE * self.grid_y

		valid_x = x > node_x - tile.GRID_SIZE // 2 and x < node_x + tile.GRID_SIZE // 2
		valid_y = y > node_y - tile.GRID_SIZE // 2 and y < node_y + tile.GRID_SIZE // 2
		return valid_x and valid_y

	def default_handler(self, command):
		pass

	def on_update(self, dt):
		pass
		
