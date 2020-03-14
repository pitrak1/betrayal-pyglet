import pyglet
from src.shared import node
from src.client.world.common import label
from src.client.world.common import area

class TextBox(node.Node):
	def __init__(self, asset, x, y, width, label_text):
		super().__init__()
		self.area = area.Area(asset, x, y, width, 2, 'left')
		self.input_label = label.Label(label_text, x=x, y=y + area.ASSET_TILE_SIZE * 2, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(0, 0, 0, 255))
		self.input_text = label.Label('', x=x, y=y, anchor_x='left', anchor_y='center', align='left', font_size=15)
		self.input_error = label.Label('', x=x, y=y - 30, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(255, 0, 0, 255))
		self.selected = False

	def set_error_text(self, text):
		self.input_error.text = text

	def get_text(self):
		return self.input_text.text

	def draw(self):
		self.area.draw()
		self.input_label.draw()
		self.input_text.draw()
		self.input_error.draw()

	def client_text_entered_handler(self, command, state):
		if self.selected:
			self.input_text.text += command.data['text']

	def client_key_press_handler(self, command, state):
		if self.selected and command.data['symbol'] == pyglet.window.key.BACKSPACE:
			self.input_text.text = self.input_text.text[:-1]

	def client_translated_mouse_press_handler(self, command, state):
		if self.area.within_bounds(command.data['x'], command.data['y']):
			self.selected = True
		else:
			self.selected = False
