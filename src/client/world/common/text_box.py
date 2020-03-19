import pyglet
from src.shared import node
from src.client.world.common import label
from src.client.world.common import area as area_module

class TextBox(area_module.Area):
	def __init__(self, asset, x, y, width, label_text, max_length):
		super().__init__(asset, x, y, width, 2, 'left')
		self.foreground = pyglet.graphics.OrderedGroup(1)

		self.document = pyglet.text.document.UnformattedDocument('')
		self.document.set_style(0, 0, dict(color=(0, 0, 0, 255), font_size=15))

		self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, width * 16, 24, multiline=False, batch=self.batch, group=self.foreground)
		self.layout.anchor_x = 'left'
		self.layout.anchor_y = 'center'
		self.layout.x = x
		self.layout.y = y

		self.caret = pyglet.text.caret.Caret(self.layout)

		self.max_length = max_length
		self.input_label = label.Label(label_text, x=x, y=y + area_module.ASSET_TILE_SIZE * 2, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(0, 0, 0, 255), batch=self.batch, group=self.foreground)
		self.input_error = label.Label('', x=x, y=y - 30, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(255, 0, 0, 255), batch=self.batch, group=self.foreground)
		self.selected = False

	def set_error_text(self, text):
		self.input_error.text = text

	def get_text(self):
		return self.document.text

	def client_text_entered_handler(self, command, state):
		if self.selected:
			self.caret.on_text(command.data['text'])
			self.__enforce_length()

	def client_text_motion_handler(self, command, state):
		if self.selected:
			self.caret.on_text_motion(command.data['motion'])
			self.__enforce_length()

	def client_text_motion_select_handler(self, command, state):
		if self.selected:
			self.caret.on_text_motion_select(command.data['motion'])
			self.__enforce_length()

	def client_translated_mouse_press_handler(self, command, state):
		if self.within_bounds(command.data['x'], command.data['y']):
			self.caret.visible = True
			self.caret.on_mouse_press(command.data['x'], command.data['y'], command.data['button'], command.data['modifiers'])
			self.selected = True
		else:
			self.caret.visible = False
			self.caret.mark = self.caret.position = 0
			self.selected = False

	def client_translated_mouse_drag_handler(self, command, state):
		if self.selected:
			self.caret.on_mouse_drag(command.data['x'], command.data['y'], command.data['dx'], command.data['dy'], command.data['buttons'], command.data['modifiers'])
			self.__enforce_length()

	def __enforce_length(self):
		if len(self.document.text) > self.max_length:
			stored_caret_position = self.caret.position
			self.document.text = self.document.text[:self.max_length]
			self.caret.mark = self.caret.position = stored_caret_position
