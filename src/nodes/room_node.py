from pyglet import window
from src.nodes import visible_node, character_node
from src.tiles import room_tile
from pyglet.window import key

class RoomNode(visible_node.VisibleNode):
	def __init__(self, state_machine, tile, grid_x, grid_y, world):
		super().__init__(state_machine, tile, grid_x, grid_y)
		self.characters = []
		self.world = world

	def on_draw(self):
		super().on_draw()

		for character in self.characters:
			character.on_draw()

	def key_press_handler(self, command):
		if self.state_machine.is_rotating(self.grid_x, self.grid_y):
			if command.symbol == key.Q:
				self.tile.rotate(1)
			elif command.symbol == key.E:
				self.tile.rotate(3)
			elif command.symbol == key.ENTER:
				if self.world.is_valid(self.grid_x, self.grid_y, self.state_machine.current_state.direction): self.state_machine.place_room()

	def mouse_press_handler(self, command):
		if self.state_machine.current_state.__class__.__name__ != 'RotatingRoomState' and self.tile.within_bounds(command.x, command.y):
			if command.button == window.mouse.LEFT:
				if not self.default_handler(command):
					self.state_machine.select(self)
			elif command.button == window.mouse.RIGHT:
				if not self.default_handler(command):
					if self.state_machine.current_state.__class__.__name__ == 'SelectedState' and self.world.can_move(self.state_machine.current_state.selected.grid_x, self.state_machine.current_state.selected.grid_y, self.grid_x, self.grid_y):
						self.state_machine.move(self.grid_x, self.grid_y)

	def add_character_handler(self, command):
		if self.grid_x == command.grid_x and self.grid_y == command.grid_y:
			character = character_node.CharacterNode(self.state_machine, command.character_tile, self.grid_x, self.grid_y)
			self.characters.append(character)

	def move_character_handler(self, command):
		if command.grid_x == self.grid_x and command.grid_y == self.grid_y:
				if command.character not in self.characters:
					command.character.grid_x = self.grid_x
					command.character.grid_y = self.grid_y
					command.character.tile.set_position(self.grid_x, self.grid_y)
					self.characters.append(command.character)
		else:
			if command.character in self.characters:
				self.characters.remove(command.character)

	def default_handler(self, command):
		return any(character.on_command(command) for character in self.characters)

	def on_update(self, dt):
		for character in self.characters:
			character.on_update(dt)
		
