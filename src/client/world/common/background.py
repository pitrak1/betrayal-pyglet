import pyglet
from src.shared import constants, node

class Background(node.Node):
	def __init__(self, image):
		super().__init__()
		self.sprite = pyglet.sprite.Sprite(image)
		self.__scale_to_window_size()

	def __scale_to_window_size(self):
		self.sprite.scale_x = constants.WINDOW_WIDTH / self.sprite.width
		self.sprite.scale_y = constants.WINDOW_HEIGHT / self.sprite.height
		self.sprite.update(x=constants.WINDOW_WIDTH / 2, y=constants.WINDOW_HEIGHT / 2)

	def draw(self):
		self.sprite.draw()	
