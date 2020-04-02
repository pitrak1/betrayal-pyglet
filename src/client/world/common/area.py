import pyglet
from src.shared import node, bounds, constants

class Area(node.Node):
	def __init__(self, asset, x, y, unit_width, unit_height, batch, group, align='center', opacity=255):
		super().__init__()
		self.x = x
		self.y = y
		self.unit_width = unit_width
		self.unit_height = unit_height
		self.sprites = []

		if align == 'center':
			base_x_offset = (unit_width - 1) / 2 * constants.AREA_TILE_SIZE
			base_y_offset = (unit_height - 1) / 2 * constants.AREA_TILE_SIZE
		elif align == 'left':
			base_x_offset = 0
			base_y_offset = (unit_height - 1) / 2 * constants.AREA_TILE_SIZE
		else:
			base_x_offset = (unit_width - 1) / 2 * constants.AREA_TILE_SIZE
			base_y_offset = (unit_height - 1) / 2 * constants.AREA_TILE_SIZE

		for j in range(unit_height):
			if j == 0:
				base_sprite_index = 0
			elif j == unit_height - 1:
				base_sprite_index = 6
			else:
				base_sprite_index = 3

			for i in range(unit_width):
				if i == 0:
					sprite_index = base_sprite_index + 0
				elif i == unit_width - 1:
					sprite_index = base_sprite_index + 2
				else:
					sprite_index = base_sprite_index + 1
				self.sprites.append(pyglet.sprite.Sprite(asset[sprite_index], batch=batch, group=group))
				self.sprites[j * unit_width + i].update(
					x=x - base_x_offset + constants.AREA_TILE_SIZE * i, 
					y=y - base_y_offset + constants.AREA_TILE_SIZE * j,
				)
				self.sprites[j * unit_width + i].opacity = opacity

	def within_bounds(self, x, y):
		return bounds.within_rect_bounds(self.x, self.y, x, y, self.unit_width * constants.AREA_TILE_SIZE, self.unit_height * constants.AREA_TILE_SIZE)
