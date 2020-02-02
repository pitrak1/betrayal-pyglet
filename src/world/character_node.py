from pyglet import sprite

class CharacterNode():
	def __init__(self, img, grid_x, grid_y, x, y):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.sprite = sprite.Sprite(img, x, y)

	def on_draw(self):
		self.sprite.draw()

	def on_command(self, command, queue):
		pass

	def on_update(self, dt):
		pass