from pyglet import window
from src import node as node_module
from src.utils import constants, bounds as bounds_module
from src.states import selected_state as selected_state_module

class EmptySpace(node_module.Node):
	def __init__(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y

	def within_bounds(self, x, y):
		return bounds_module.within_square_bounds(self.grid_x * constants.GRID_SIZE, self.grid_y * constants.GRID_SIZE, x, y, constants.GRID_SIZE)

	def on_draw(self, state):
		pass

	def translated_mouse_press_handler(self, command, state):
		if state.__class__ == selected_state_module.SelectedState:
			if command.button == window.mouse.RIGHT and self.within_bounds(command.x, command.y):
				state.trigger_selected_character_move(self.grid_x, self.grid_y, False)

	def default_handler(self, command, state):
		pass

	def on_update(self, dt, state):
		pass
		
