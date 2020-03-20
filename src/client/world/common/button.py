import pyglet
from src.shared import node
from src.client.world.common import area, label

class Button(node.Node):
	def __init__(self, asset, x, y, unit_width, unit_height, text, on_click, batch, area_group, text_group):
		super().__init__()
		self.__area = area.Area(asset, x, y, unit_width, unit_height, batch=batch, group=area_group)
		self.__on_click = on_click
		self.__label = label.Label(text, x=x, y=y, anchor_x='center', anchor_y='center', align='center', font_size=15, color=(0, 0, 0, 255), batch=batch, group=text_group)

	def client_translated_mouse_press_handler(self, command, state=None):
		if self.__area.within_bounds(command.data['x'], command.data['y']):
			self.__on_click()	
