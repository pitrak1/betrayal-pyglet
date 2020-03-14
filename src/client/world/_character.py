from pyglet import window
from src import node as node_module
from src.states import no_selection_state as no_selection_state_module, selected_state as selected_state_module

class Character(node_module.Node):
	def __init__(self, tile, grid_x, grid_y):
		self.tile = tile
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.tile.set_position(grid_x, grid_y)
		self.selected = False

	def on_draw(self, state):
		self.tile.on_draw(self.selected)

	def translated_mouse_press_handler(self, command, state):
		if state.name(['SelectedState', 'NoSelectionState']):
			if command.button == window.mouse.LEFT and self.tile.within_bounds(command.x, command.y):
				state.select(self)
				return True
			else:
				return False

	def select_handler(self, command, state):
		self.selected = command.selected == self

	def default_handler(self, command, state):
		pass

	def on_update(self, dt, state):
		pass

	
