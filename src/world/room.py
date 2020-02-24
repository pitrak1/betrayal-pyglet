from pyglet import window
from src import node as node_module
from pyglet.window import key
from src.states import selected_state as selected_state_module
from src.world import character as character_module

class Room(node_module.Node):
	def __init__(self, tile, grid_x, grid_y):
		self.tile = tile
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.tile.set_position(grid_x, grid_y)
		self.characters = []
		self.selected = False

	def on_draw(self, state):
		self.tile.on_draw(self.selected)

		for character in self.characters:
			character.on_draw(state)

	def select_handler(self, command, state):
		self.selected = command.selected == self
		self.default_handler(command, state)

	def place_character_handler(self, command, state):
		if self.grid_x == command.grid_x and self.grid_y == command.grid_y:
			character = character_module.Character(command.character_tile, self.grid_x, self.grid_y)
			self.characters.append(character)


	def key_press_handler(self, command, state):
		if state.name('RotatingRoomState') and state.is_rotating(self.grid_x, self.grid_y):
			if command.symbol == key.Q:
				self.tile.doors.rotate(1)
			elif command.symbol == key.E:
				self.tile.doors.rotate(3)
			elif command.symbol == key.ENTER:
				state.trigger_stop_room_rotating()

	def translated_mouse_press_handler(self, command, state):
		if self.tile.within_bounds(command.x, command.y):
			if command.button == window.mouse.LEFT and state.name(['SelectedState', 'NoSelectionState']):
				if not self.default_handler(command, state):
					state.select(self)
			elif command.button == window.mouse.RIGHT and state.name('SelectedState'):
				if not self.default_handler(command, state):
					state.trigger_selected_character_move(self.grid_x, self.grid_y, True)

	def move_character_handler(self, command, state):
		if command.end_x == self.grid_x and command.end_y == self.grid_y:
				if command.character not in self.characters:
					command.character.grid_x = self.grid_x
					command.character.grid_y = self.grid_y
					command.character.tile.set_position(self.grid_x, self.grid_y)
					self.characters.append(command.character)
		else:
			if command.character in self.characters:
				self.characters.remove(command.character)

	def default_handler(self, command, state):
		return any(character.on_command(command, state) for character in self.characters)

	def on_update(self, dt, state):
		for character in self.characters:
			character.on_update(dt, state)
		
