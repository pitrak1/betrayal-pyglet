import pyglet
from src.common import node, constants, logger
from src.client.common import label, area

class TextBox(area.Area):
	def __init__(self, asset, x, y, unit_width, label_text, max_length, batch, area_group, text_group):
		super().__init__(asset, x, y, unit_width, 2, align='left', batch=batch, group=area_group)
		self.label_text = label_text
		self.document = pyglet.text.document.UnformattedDocument('')
		self.document.set_style(0, 0, dict(color=(0, 0, 0, 255), font_size=15))

		self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, unit_width * 16, 24, multiline=False, batch=batch, group=text_group)
		self.layout.anchor_x = 'left'
		self.layout.anchor_y = 'center'
		self.layout.x = x
		self.layout.y = y

		self.caret = pyglet.text.caret.Caret(self.layout)

		self.max_length = max_length
		self.input_label = label.Label(label_text, x=x, y=y + constants.AREA_TILE_SIZE * 2, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(0, 0, 0, 255), batch=batch, group=text_group)
		self.input_error = label.Label('', x=x, y=y - 30, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(255, 0, 0, 255), batch=batch, group=text_group)
		self.selected = False

	def set_error_text(self, text):
		self.input_error.text = text

	def get_text(self):
		return self.document.text

	def client_text_entered_handler(self, command, state):
		logger.log(f'TextBox {self.label_text} handling command', logger.LOG_LEVEL_COMMAND)
		if self.selected:
			logger.log(f'TextBox {self.label_text} is selected, acting', logger.LOG_LEVEL_DEBUG)
			self.caret.on_text(command.data['text'])
			self.enforce_length()

	def client_text_motion_handler(self, command, state):
		logger.log(f'TextBox {self.label_text} handling command', logger.LOG_LEVEL_COMMAND)
		if self.selected:
			logger.log(f'TextBox {self.label_text} is selected, acting', logger.LOG_LEVEL_DEBUG)
			self.caret.on_text_motion(command.data['motion'])
			self.enforce_length()

	def client_text_motion_select_handler(self, command, state):
		logger.log(f'TextBox {self.label_text} handling command', logger.LOG_LEVEL_COMMAND)
		if self.selected:
			logger.log(f'TextBox {self.label_text} is selected, acting', logger.LOG_LEVEL_DEBUG)
			self.caret.on_text_motion_select(command.data['motion'])
			self.enforce_length()

	def client_mouse_press_handler(self, command, state):
		logger.log(f'TextBox {self.label_text} handling command', logger.LOG_LEVEL_COMMAND)
		if self.within_bounds(command.data['x'], command.data['y']):
			logger.log(f'Within bounds of TextBox {self.label_text}, selecting', logger.LOG_LEVEL_DEBUG)
			self.caret.visible = True
			self.caret.on_mouse_press(command.data['x'], command.data['y'], command.data['button'], command.data['modifiers'])
			self.selected = True
		else:
			logger.log(f'Not within bounds of TextBox {self.label_text}, unselecting', logger.LOG_LEVEL_DEBUG)
			self.caret.visible = False
			self.caret.mark = self.caret.position = 0
			self.selected = False

	def client_mouse_drag_handler(self, command, state):
		logger.log(f'TextBox {self.label_text} handling command', logger.LOG_LEVEL_COMMAND)
		if self.selected:
			logger.log(f'TextBox {self.label_text} is selected, acting', logger.LOG_LEVEL_DEBUG)
			self.caret.on_mouse_drag(command.data['x'], command.data['y'], command.data['dx'], command.data['dy'], command.data['buttons'], command.data['modifiers'])
			self.enforce_length()

	def enforce_length(self):
		if len(self.document.text) > self.max_length:
			stored_caret_position = self.caret.position
			self.document.text = self.document.text[:self.max_length]
			self.caret.mark = self.caret.position = stored_caret_position
