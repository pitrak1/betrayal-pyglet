import pyglet
from src.shared import constants, node

class Background(node.Node):
	def __init__(self, asset, batch, group):
		super().__init__()
		self.__sprite = pyglet.sprite.Sprite(asset, batch=batch, group=group)
		self.__scale_to_window_size()

	def __scale_to_window_size(self):
		self.__sprite.scale_x = constants.WINDOW_WIDTH / self.__sprite.width
		self.__sprite.scale_y = constants.WINDOW_HEIGHT / self.__sprite.height
		self.__sprite.update(x=constants.WINDOW_WIDTH / 2, y=constants.WINDOW_HEIGHT / 2)
