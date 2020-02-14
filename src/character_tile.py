import math
from pyglet import sprite, text
from src import assets

ROOM_SIZE = 512
CHARACTER_SIZE = 150

class CharacterTile():
	def __init__(self, images, name, asset):
		self.name = name
		self.sprite = sprite.Sprite(images[asset])
		self.selected = sprite.Sprite(images['character_selected'])
		self.label = text.Label(name)

	def set_position(self, grid_x, grid_y):
		x = grid_x * ROOM_SIZE
		y = grid_y * ROOM_SIZE

		self.sprite.update(x=x, y=y)
		self.selected.update(x=x, y=y)

		self.label.x = x
		self.label.y = y


	def on_draw(self, is_selected):
		self.sprite.draw()
		if is_selected: self.selected.draw()
		self.label.draw()

	def within_bounds(self, x, y):
		distance = math.sqrt(((self.sprite.x - x) ** 2) + ((self.sprite.y - y) ** 2 ))
		return distance < CHARACTER_SIZE // 2
