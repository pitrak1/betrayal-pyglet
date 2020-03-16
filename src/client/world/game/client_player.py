import pyglet
from src.client.world.game import client_character as client_character_module
from src.shared import bounds, constants

class ClientPlayer(client_character_module.ClientCharacter):
	def __init__(self, entry, asset_manager, name, grid_x, grid_y):
		super().__init__(entry, asset_manager)
		self.name = name
		self.grid_x = grid_x	
		self.grid_y = grid_y

	def client_translated_mouse_press_handler(self, command, state):
		if self.within_bounds(command.data['x'], command.data['y']):
			if command.data['button'] == pyglet.window.mouse.LEFT:
				state.select(self)
				return True
			# elif command.data['button'] == window.mouse.RIGHT and state.name('SelectedState'):
			# 	if not self.default_handler(command, state):
			# 		state.trigger_selected_character_move(self.grid_x, self.grid_y, True)

	def client_select_handler(self, command, state):
		self.selected = command.data['selected'] == self

	def within_bounds(self, x, y):
		return bounds.within_circle_bounds(self.grid_x * constants.GRID_SIZE, self.grid_y * constants.GRID_SIZE, x, y, constants.CHARACTER_SIZE)

