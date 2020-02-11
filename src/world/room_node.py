from pyglet import sprite, window
from src.commands import commands
from src.world import character_node

ROOM_SIZE = 512

class RoomNode():
	def __init__(self, img, img_selected, grid_x, grid_y, state_machine):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.sprite = sprite.Sprite(img, grid_x * ROOM_SIZE, grid_y * ROOM_SIZE)
		self.sprite_selected = sprite.Sprite(img_selected, grid_x * ROOM_SIZE, grid_y * ROOM_SIZE)
		self.state_machine = state_machine
		self.characters = []


	def on_draw(self):
		if self.state_machine.is_selected(self):
			self.sprite_selected.draw() 
		else:
			self.sprite.draw()

		for character in self.characters:
			character.on_draw()

	def on_command(self, command, state_machine):
		if isinstance(command, commands.AddCharacterCommand) \
				and self.grid_x == command.grid_x and self.grid_y == command.grid_y:
			self.__add_character(command)
		elif isinstance(command, commands.MousePressCommand) \
			and self.__within_bounds(command.x, command.y):
				if command.button == window.mouse.LEFT:
					hit_flag = False
					for character in self.characters:
						if character.on_command(command, state_machine):
							hit_flag = True

					if not hit_flag:
						state_machine.select(self)
				elif command.button == window.mouse.RIGHT:
					pass
		else:
			for character in self.characters:
				character.on_command(command, state_machine)

	def on_update(self, dt):
		for character in self.characters:
			character.on_update(dt)

	def __add_character(self, command):
		x = self.sprite.x
		y = self.sprite.y
		character = character_node.CharacterNode(command.img, command.img_selected, self.grid_x, self.grid_y, x, y, self.state_machine)
		self.characters.append(character)

	def __within_bounds(self, x, y):
		valid_x = x > self.sprite.x - ROOM_SIZE // 2 and x < self.sprite.x + ROOM_SIZE // 2
		valid_y = y > self.sprite.y - ROOM_SIZE // 2 and y < self.sprite.y + ROOM_SIZE // 2
		return valid_x and valid_y
