import math
from pyglet import sprite, window
from src.commands import mouse_press_command, highlight_command

CHARACTER_SIZE = 150

class CharacterNode():
	def __init__(self, img, img_highlighted, grid_x, grid_y, x, y):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.sprite = sprite.Sprite(img, x, y)
		self.sprite_highlighted = sprite.Sprite(img_highlighted, x, y)
		self.highlighted = False

	def on_draw(self):
		self.sprite_highlighted.draw() if self.highlighted else self.sprite.draw()

	def on_command(self, command, queue):
		if isinstance(command, mouse_press_command.MousePressCommand):
			return self.__mouse_press_handler(command, queue)
		elif isinstance(command, highlight_command.HighlightCommand):
			return self.__highlight_handler(command, queue)

	def __mouse_press_handler(self, command, queue):
		if command.button == window.mouse.LEFT:
			if self.__within_bounds(command.x, command.y):
				queue.append(highlight_command.HighlightCommand(self))
				return True
			return False
		elif command.button == window.mouse.RIGHT:
			pass

	def __within_bounds(self, x, y):
		distance = math.sqrt(((self.sprite.x - x) ** 2) + ((self.sprite.y - y) ** 2 ))
		return distance < CHARACTER_SIZE // 2

	def __highlight_handler(self, command, queue):
		if command.node == self:
			self.highlighted = True
		else:
			self.highlighted = False

	def on_update(self, dt):
		pass

	
