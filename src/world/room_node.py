from pyglet import sprite
from src.commands import add_character_command
from src.world import character_node

ROOM_SIZE = 512

class RoomNode():
	def __init__(self, img, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.sprite = sprite.Sprite(img, grid_x * ROOM_SIZE, grid_y * ROOM_SIZE)
		self.characters = []


	def on_draw(self):
		self.sprite.draw()

		for character in self.characters:
			character.on_draw()

	def on_command(self, command, queue):
		if isinstance(command, add_character_command.AddCharacterCommand) \
				and self.grid_x == command.grid_x and self.grid_y == command.grid_y:
			self.__add_character(command)
		else:
			for character in self.characters:
				character.on_command(command, queue)

	def on_update(self, dt):
		for character in self.characters:
			character.on_update(dt)

	def __add_character(self, command):
		x = self.sprite.x
		y = self.sprite.y
		character = character_node.CharacterNode(command.img, self.grid_x, self.grid_y, x, y)
		self.characters.append(character)