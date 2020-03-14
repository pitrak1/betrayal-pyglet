import pyglet
from src.utils import constants

class Tile():
	def __init__(self, name, image, image_selected):
		self.name = name
		self.label = pyglet.text.Label(name)
		self.sprite = pyglet.sprite.Sprite(image)
		self.selected = pyglet.sprite.Sprite(image_selected)
		self.grid_x = 0
		self.grid_y = 0

	def set_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.sprite.update(x=grid_x * constants.GRID_SIZE, y=grid_y * constants.GRID_SIZE)
		self.selected.update(x=grid_x * constants.GRID_SIZE, y=grid_y * constants.GRID_SIZE)

		self.label.x = grid_x * constants.GRID_SIZE
		self.label.y = grid_y * constants.GRID_SIZE

	def on_draw(self, is_selected):
		self.sprite.draw()
		if is_selected: self.selected.draw()
		self.label.draw()

	def within_bounds(self, x, y):
		raise NotImplementedError('within_bounds must be overridden')
