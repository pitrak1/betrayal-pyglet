from pyglet import window
from src.nodes import visible_node, character_node
from src.tiles import room_tile
from pyglet.window import key

class RoomNode(visible_node.VisibleNode):
	def __init__(self, state_machine, tile, grid_position, world):
		super().__init__(state_machine, tile, grid_position)
		self.characters = []
		self.world = world

	def on_draw(self):
		super().on_draw()

		for character in self.characters:
			character.on_draw()

	def key_press_handler(self, command):
		if self.state_machine.is_rotating(self.grid_position):
			if command.symbol == key.Q:
				self.tile.doors.rotate(1)
			elif command.symbol == key.E:
				self.tile.doors.rotate(3)
			elif command.symbol == key.ENTER:
				if self.world.is_room_rotation_valid(self.grid_position, self.state_machine.current_state.direction): 
					self.state_machine.place_room()

	def mouse_press_handler(self, command):
		if self.state_machine.current_state.__class__.__name__ != 'RotatingRoomState' and self.tile.within_bounds(command.position):
			if command.button == window.mouse.LEFT:
				if not self.default_handler(command):
					self.state_machine.select(self)
			elif command.button == window.mouse.RIGHT:
				if not self.default_handler(command):
					if self.state_machine.current_state.__class__.__name__ == 'SelectedState' and self.world.can_move(self.state_machine.current_state.selected.grid_position, self.grid_position):
						self.state_machine.move(self.grid_position)

	def add_character_handler(self, command):
		if self.grid_position == command.grid_position:
			character = character_node.CharacterNode(self.state_machine, command.character_tile, self.grid_position)
			self.characters.append(character)

	def move_character_handler(self, command):
		if command.grid_position == self.grid_position:
				if command.character not in self.characters:
					command.character.grid_position = self.grid_position.copy()
					command.character.tile.set_position(self.grid_position)
					self.characters.append(command.character)
		else:
			if command.character in self.characters:
				self.characters.remove(command.character)

	def default_handler(self, command):
		return any(character.on_command(command) for character in self.characters)

	def on_update(self, dt):
		for character in self.characters:
			character.on_update(dt)
		
