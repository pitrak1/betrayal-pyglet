import math
from pyglet import sprite
from src.tiles import tile

CHARACTER_SIZE = 150

class CharacterTile(tile.Tile):
	def __init__(self, name, images, asset):
		super().__init__(name, images[asset], images['character_selected'])

	def within_bounds(self, position):
		return self.grid_position.within_circle_bounds(position, CHARACTER_SIZE)
