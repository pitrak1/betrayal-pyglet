import math
from pyglet import sprite
from src.tiles import tile

CHARACTER_SIZE = 150

class CharacterTile(tile.Tile):
	def __init__(self, name, images, asset):
		super().__init__(name, images[asset], images['character_selected'])

	def within_bounds(self, x, y):
		distance = math.sqrt(((self.sprite.x - x) ** 2) + ((self.sprite.y - y) ** 2 ))
		return distance < CHARACTER_SIZE // 2
