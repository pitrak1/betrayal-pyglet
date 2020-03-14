import pyglet
from src.shared import node
from src.client.world.common import area as area_module

class Button(node.Node):
	def __init__(self, asset, x, y, width, height, text, on_click):
		super().__init__()
		self.area = area_module.Area(asset, x, y, width, height)
		self.on_click = on_click
		self.label = pyglet.text.Label(text, x=x, y=y, anchor_x='center', anchor_y='center', align='center', font_size=15, color=(0, 0, 0, 255))

	def draw(self):
		self.area.draw()
		self.label.draw()

	def client_translated_mouse_press_handler(self, command, state=None):
		if self.area.within_bounds(command.data['x'], command.data['y']):
			self.on_click()	
