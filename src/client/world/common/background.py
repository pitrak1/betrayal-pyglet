import pyglet
from src.shared import constants, node

class Background(node.Node):
	def __init__(self, asset, batch, group):
		super().__init__()
		self.sprite = pyglet.sprite.Sprite(asset, batch=batch, group=group)
		self.scale_to_window_size()

	def scale_to_window_size(self):
		self.sprite.scale_x = constants.WINDOW_WIDTH / self.sprite.width
		self.sprite.scale_y = constants.WINDOW_HEIGHT / self.sprite.height
		self.sprite.update(x=constants.WINDOW_WIDTH / 2, y=constants.WINDOW_HEIGHT / 2)
