from pyglet import sprite, window
from src.commands import commands
from src.world import character_node
from src import room_tile

class RoomNode():
	def __init__(self, room_tile, grid_x, grid_y, state_machine):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.room_tile = room_tile
		self.room_tile.set_position(grid_x, grid_y)
		self.state_machine = state_machine
		self.characters = []


	def on_draw(self):
		self.room_tile.on_draw(self.state_machine.is_selected(self))

		for character in self.characters:
			character.on_draw()

	def on_command(self, command):
		if isinstance(command, commands.AddCharacterCommand) \
				and self.grid_x == command.grid_x and self.grid_y == command.grid_y:
			self.__add_character(command)
		elif isinstance(command, commands.MousePressCommand) \
			and self.room_tile.within_bounds(command.x, command.y):
				if command.button == window.mouse.LEFT:
					hit_flag = False
					for character in self.characters:
						if character.on_command(command):
							hit_flag = True

					if not hit_flag:
						self.state_machine.select(self)
				elif command.button == window.mouse.RIGHT:
					hit_flag = False
					for character in self.characters:
						if character.on_command(command):
							hit_flag = True

					if not hit_flag:
						self.state_machine.move(self)
		elif isinstance(command, commands.MoveCharacterCommand):
			if command.room == self:
				if command.character not in self.characters:
					self.__place_character(command)
			else:
				if command.character in self.characters:
					self.characters.remove(command.character)
		else:
			for character in self.characters:
				character.on_command(command)

	def on_update(self, dt):
		for character in self.characters:
			character.on_update(dt)

	def __add_character(self, command):
		character = character_node.CharacterNode(command.character_tile, self.grid_x, self.grid_y, self.state_machine)
		self.characters.append(character)

	def __place_character(self, command):
		command.character.grid_x = self.grid_x
		command.character.grid_y = self.grid_y
		command.character.character_tile.set_position(self.grid_x, self.grid_y)
		self.characters.append(command.character)
