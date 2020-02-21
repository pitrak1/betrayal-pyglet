from pyglet import window
from src.nodes import visible_node, character_node
from src.tiles import room_tile
from pyglet.window import key
from src.states import selected_state as selected_state_module, rotating_room_state as rotating_room_state_module

class RoomNode(visible_node.VisibleNode):
	def __init__(self, tile, grid_position, world):
		super().__init__(tile, grid_position)
		self.characters = []
		self.world = world

	def on_draw(self, state):
		super().on_draw(state)

		for character in self.characters:
			character.on_draw(state)

	def key_press_handler(self, command, state):
		if state.__class__ == rotating_room_state_module.RotatingRoomState and state.is_rotating(self.grid_position):
			if command.symbol == key.Q:
				self.tile.doors.rotate(1)
			elif command.symbol == key.E:
				self.tile.doors.rotate(3)
			elif command.symbol == key.ENTER:
				if self.world.is_room_rotation_valid(self.grid_position, state.entering_direction): 
					state.place_room()

	def translated_mouse_press_handler(self, command, state):
		if state.__class__ != rotating_room_state_module.RotatingRoomState and self.tile.within_bounds(command.position):
			if command.button == window.mouse.LEFT:
				if not self.default_handler(command, state):
					state.select(self)
			elif command.button == window.mouse.RIGHT:
				if not self.default_handler(command, state):
					if state.__class__ == selected_state_module.SelectedState and self.world.can_move(state.selected.grid_position, self.grid_position):
						state.move(self.grid_position)

	def add_character_handler(self, command, state):
		if self.grid_position == command.grid_position:
			character = character_node.CharacterNode(command.character_tile, self.grid_position)
			self.characters.append(character)

	def move_character_handler(self, command, state):
		if command.grid_position == self.grid_position:
				if command.character not in self.characters:
					command.character.grid_position = self.grid_position.copy()
					command.character.tile.set_position(self.grid_position)
					self.characters.append(command.character)
		else:
			if command.character in self.characters:
				self.characters.remove(command.character)

	def default_handler(self, command, state):
		return any(character.on_command(command, state) for character in self.characters)

	def on_update(self, dt, state):
		for character in self.characters:
			character.on_update(dt, state)
		
