from pyglet import window
from src.nodes import visible_node, character_node

class RoomNode(visible_node.VisibleNode):
	def __init__(self, state_machine, tile, grid_x, grid_y):
		super().__init__(state_machine, tile, grid_x, grid_y)
		self.characters = []


	def on_draw(self):
		super().on_draw()

		for character in self.characters:
			character.on_draw()

	def mouse_press_handler(self, command):
		if self.tile.within_bounds(command.x, command.y):
			if command.button == window.mouse.LEFT:
				if not self.default_handler(command):
					self.state_machine.select(self)
			elif command.button == window.mouse.RIGHT:
				if not self.default_handler(command):
					self.state_machine.move(self)

	def add_character_handler(self, command):
		if self.grid_x == command.grid_x and self.grid_y == command.grid_y:
			character = character_node.CharacterNode(self.state_machine, command.character_tile, self.grid_x, self.grid_y)
			self.characters.append(character)

	def move_character_handler(self, command):
		if command.room == self:
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
		
