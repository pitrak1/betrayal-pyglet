from pyglet import sprite, text

GRID_SIZE = 512

class Tile():
	def __init__(self, name, image, image_selected):
		self.name = name
		self.label = text.Label(name)
		self.sprite = sprite.Sprite(image)
		self.selected = sprite.Sprite(image_selected)

	def set_position(self, grid_x, grid_y):
		x = grid_x * GRID_SIZE
		y = grid_y * GRID_SIZE

		self.sprite.update(x=x, y=y)
		self.selected.update(x=x, y=y)

		self.label.x = x
		self.label.y = y

	def on_draw(self, is_selected):
		self.sprite.draw()
		if is_selected: self.selected.draw()
		self.label.draw()

	def within_bounds(self, x, y):
		raise NotImplementedError('within_bounds must be overridden')
