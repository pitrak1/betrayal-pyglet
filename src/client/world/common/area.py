import pyglet
from src.shared import node

ASSET_TILE_SIZE = 16

class Area(node.Node):
	def __init__(self, asset, x, y, width, height, align='center', opacity=255):
		super().__init__()
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.sprites = []
		self.batch = pyglet.graphics.Batch()

		if align == 'center':
			base_x_offset = (width - 1) / 2 * ASSET_TILE_SIZE
			base_y_offset = (height - 1) / 2 * ASSET_TILE_SIZE
		elif align == 'left':
			base_x_offset = 0
			base_y_offset = (height - 1) / 2 * ASSET_TILE_SIZE
		else:
			base_x_offset = (width - 1) / 2 * ASSET_TILE_SIZE
			base_y_offset = (height - 1) / 2 * ASSET_TILE_SIZE

		for j in range(height):
			if j == 0:
				base_sprite_index = 0
			elif j == height - 1:
				base_sprite_index = 6
			else:
				base_sprite_index = 3

			for i in range(width):
				if i == 0:
					sprite_index = base_sprite_index + 0
				elif i == width - 1:
					sprite_index = base_sprite_index + 2
				else:
					sprite_index = base_sprite_index + 1
				self.sprites.append(pyglet.sprite.Sprite(asset[sprite_index], batch=self.batch))
				self.sprites[j * width + i].update(
					x=x - base_x_offset + ASSET_TILE_SIZE * i, 
					y=y - base_y_offset + ASSET_TILE_SIZE * j,
				)
				self.sprites[j * width + i].opacity = opacity

	def draw(self):
		self.batch.draw()

	def within_bounds(self, x, y):
		base_x_offset = self.width / 2 * ASSET_TILE_SIZE
		base_y_offset = self.height / 2 * ASSET_TILE_SIZE
		x_valid = x > self.x - base_x_offset and x < self.x + base_x_offset
		y_valid = y > self.y - base_y_offset and y < self.y + base_y_offset
		return x_valid and y_valid	
