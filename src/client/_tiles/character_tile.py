import math
from src.tiles import tile
from src.utils import constants, bounds as bounds_module

class CharacterTile(tile.Tile):
	def within_bounds(self, x, y):
		return bounds_module.within_circle_bounds(self.sprite.x, self.sprite.y, x, y, constants.CHARACTER_SIZE)
