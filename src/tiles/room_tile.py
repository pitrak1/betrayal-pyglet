import pyglet
from src.tiles import tile, door_pattern
from src.utils import grid_position

class RoomTile(tile.Tile):
	def __init__(self, name, images, room_number, code):
		super().__init__(name, images['rooms'][room_number], images['room_selected'])
		self.doors = door_pattern.DoorPattern(code)
		self.door_sprites = [
			pyglet.sprite.Sprite(images['door']),
			pyglet.sprite.Sprite(images['door']), 
			pyglet.sprite.Sprite(images['door']), 
			pyglet.sprite.Sprite(images['door'])
		]

	def set_position(self, grid_position):
		super().set_position(grid_position)
		for i in range(4):
			door_position = grid_position.get_door_position(i)
			self.door_sprites[i].update(x=door_position.x, y=door_position.y, rotation=90 * i)

	def on_draw(self, is_selected):
		super().on_draw(is_selected)

		for i in range(4):
			if self.doors[i]: self.door_sprites[i].draw()

	def within_bounds(self, position):
		return self.grid_position.within_square_bounds(position, grid_position.GRID_SIZE)
