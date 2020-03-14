import pyglet
from src.tiles import tile as tile_module, door_pattern as door_pattern_module
from src.utils import constants, grid as grid_module, bounds as bounds_module

class RoomTile(tile_module.Tile):
	def __init__(self, name, image, image_selected, image_door, code):
		super().__init__(name, image, image_selected)
		self.doors = door_pattern_module.DoorPattern(code)
		self.door_sprites = [
			pyglet.sprite.Sprite(image_door),
			pyglet.sprite.Sprite(image_door), 
			pyglet.sprite.Sprite(image_door), 
			pyglet.sprite.Sprite(image_door)
		]

	def set_position(self, grid_x, grid_y):
		super().set_position(grid_x, grid_y)
		for i in range(4):
			door_position = grid_module.get_door_position(grid_x, grid_y, i)
			self.door_sprites[i].update(x=door_position['x'], y=door_position['y'], rotation=90 * i)

	def on_draw(self, is_selected):
		super().on_draw(is_selected)

		for i in range(4):
			if self.doors[i]: self.door_sprites[i].draw()

	def within_bounds(self, x, y):
		return bounds_module.within_square_bounds(self.sprite.x, self.sprite.y, x, y, constants.GRID_SIZE)
