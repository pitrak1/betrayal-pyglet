import pyglet
from src.utils import grid_position as grid_position_module

class Tile():
	def __init__(self, name, image, image_selected):
		self.name = name
		self.label = pyglet.text.Label(name)
		self.sprite = pyglet.sprite.Sprite(image)
		self.selected = pyglet.sprite.Sprite(image_selected)
		self.grid_position = grid_position_module.GridPosition(0, 0)

	def set_position(self, grid_position):
		self.grid_position = grid_position
		self.sprite.update(x=grid_position.x, y=grid_position.y)
		self.selected.update(x=grid_position.x, y=grid_position.y)

		self.label.x = grid_position.x
		self.label.y = grid_position.y

	def on_draw(self, is_selected):
		self.sprite.draw()
		if is_selected: self.selected.draw()
		self.label.draw()

	def within_bounds(self, position):
		raise NotImplementedError('within_bounds must be overridden')
