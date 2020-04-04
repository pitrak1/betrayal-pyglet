import pyglet
from src.shared import node, logger
from src.client.world.common import area, label

class Button(node.Node):
	def __init__(self, asset, x, y, unit_width, unit_height, text, on_click, batch, area_group, text_group):
		super().__init__()
		self.text = text
		self.area = area.Area(asset, x, y, unit_width, unit_height, batch=batch, group=area_group)
		self.on_click = on_click
		self.label = label.Label(text, x=x, y=y, anchor_x='center', anchor_y='center', align='center', font_size=15, color=(0, 0, 0, 255), batch=batch, group=text_group)

	def client_translated_mouse_press_handler(self, command, state=None):
		logger.log(f'Button {self.text} handling command', logger.LOG_LEVEL_COMMAND)
		if self.area.within_bounds(command.data['x'], command.data['y']):
			logger.log(f'Within bounds of Button {self.text}, calling on_click', logger.LOG_LEVEL_DEBUG)
			self.on_click()
