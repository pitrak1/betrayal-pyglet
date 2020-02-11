from pyglet import sprite, window
from src.commands import add_character_command, mouse_press_command, highlight_command
from src.world import character_node

ROOM_SIZE = 512

class RoomNode():
	def __init__(self, img, img_highlighted, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.sprite = sprite.Sprite(img, grid_x * ROOM_SIZE, grid_y * ROOM_SIZE)
		self.sprite_highlighted = sprite.Sprite(img_highlighted, grid_x * ROOM_SIZE, grid_y * ROOM_SIZE)
		self.highlighted = False
		self.characters = []


	def on_draw(self):
		self.sprite_highlighted.draw() if self.highlighted else self.sprite.draw()

		for character in self.characters:
			character.on_draw()

	def on_command(self, command, queue):
		if isinstance(command, add_character_command.AddCharacterCommand) \
				and self.grid_x == command.grid_x and self.grid_y == command.grid_y:
			self.__add_character(command)
		elif isinstance(command, mouse_press_command.MousePressCommand) \
			and self.__within_bounds(command.x, command.y):
				if command.button == window.mouse.LEFT:
					hit_flag = False
					for character in self.characters:
						if character.on_command(command, queue):
							hit_flag = True

					if not hit_flag:
						queue.append(highlight_command.HighlightCommand(self))
				elif command.button == window.mouse.RIGHT:
					pass
		elif isinstance(command, highlight_command.HighlightCommand):
			if command.node == self:
				self.highlighted = True
			else:
				self.highlighted = False

			for character in self.characters:
				character.on_command(command, queue)
		else:
			for character in self.characters:
				character.on_command(command, queue)

	def on_update(self, dt):
		for character in self.characters:
			character.on_update(dt)

	def __add_character(self, command):
		x = self.sprite.x
		y = self.sprite.y
		character = character_node.CharacterNode(command.img, command.img_highlighted, self.grid_x, self.grid_y, x, y)
		self.characters.append(character)

	def __within_bounds(self, x, y):
		valid_x = x > self.sprite.x - ROOM_SIZE // 2 and x < self.sprite.x + ROOM_SIZE // 2
		valid_y = y > self.sprite.y - ROOM_SIZE // 2 and y < self.sprite.y + ROOM_SIZE // 2
		return valid_x and valid_y
