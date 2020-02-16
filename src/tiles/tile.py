from pyglet import sprite, text
from src.utils import grid_position

class Tile():
	def __init__(self, name, image, image_selected):
		self.name = name
		self.label = text.Label(name)
		self.sprite = sprite.Sprite(image)
		self.selected = sprite.Sprite(image_selected)
		self.grid_position = grid_position.GridPosition(0, 0)

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
