import math
from pyglet import sprite, window
from src.commands import commands

CHARACTER_SIZE = 150

class CharacterNode():
	def __init__(self, img, img_selected, grid_x, grid_y, x, y, state_machine):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.sprite = sprite.Sprite(img, x, y)
		self.sprite_selected = sprite.Sprite(img_selected, x, y)
		self.state_machine = state_machine

	def on_draw(self):
		if self.state_machine.is_selected(self):
			self.sprite_selected.draw()
		else:
			self.sprite.draw()

	def on_command(self, command, state_machine):
		if isinstance(command, commands.MousePressCommand):
			return self.__mouse_press_handler(command, state_machine)

	def __mouse_press_handler(self, command, state_machine):
		if command.button == window.mouse.LEFT:
			if self.__within_bounds(command.x, command.y):
				state_machine.select(self)
				return True
			return False
		elif command.button == window.mouse.RIGHT:
			pass

	def __within_bounds(self, x, y):
		distance = math.sqrt(((self.sprite.x - x) ** 2) + ((self.sprite.y - y) ** 2 ))
		return distance < CHARACTER_SIZE // 2

	def on_update(self, dt):
		pass

	
