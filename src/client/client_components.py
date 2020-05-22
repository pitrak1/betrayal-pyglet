import pyglet
from src.common import constants
from lattice2d.nodes import Node
from lattice2d.utilities.bounds import within_rect_bounds

class Area(Node):
	def __init__(self, asset, x, y, unit_width, unit_height, batch, group, align='center'):
		super().__init__()
		self.x = x
		self.y = y
		self.unit_width = unit_width
		self.unit_height = unit_height
		self.sprites = []

		if align == 'left':
			base_x_offset = 0
			base_y_offset = (unit_height - 1) / 2 * constants.AREA_TILE_SIZE
		else:
			base_x_offset = (unit_width - 1) / 2 * constants.AREA_TILE_SIZE
			base_y_offset = (unit_height - 1) / 2 * constants.AREA_TILE_SIZE

		for j in range(unit_height):
			if j == 0:
				base_sprite_index = 0
			elif j == unit_height - 1:
				base_sprite_index = 6
			else:
				base_sprite_index = 3

			for i in range(unit_width):
				if i == 0:
					sprite_index = base_sprite_index + 0
				elif i == unit_width - 1:
					sprite_index = base_sprite_index + 2
				else:
					sprite_index = base_sprite_index + 1
				self.sprites.append(pyglet.sprite.Sprite(asset[sprite_index], batch=batch, group=group))
				self.sprites[j * unit_width + i].update(
					x=x - base_x_offset + constants.AREA_TILE_SIZE * i, 
					y=y - base_y_offset + constants.AREA_TILE_SIZE * j,
				)

	def within_bounds(self, x, y):
		return within_rect_bounds(self.x, self.y, x, y, self.unit_width * constants.AREA_TILE_SIZE, self.unit_height * constants.AREA_TILE_SIZE)

class Background(Node):
	def __init__(self, asset, batch, group):
		super().__init__()
		self.sprite = pyglet.sprite.Sprite(asset, batch=batch, group=group)
		self.scale_to_window_size()

	def scale_to_window_size(self):
		self.sprite.scale_x = constants.WINDOW_WIDTH / self.sprite.width
		self.sprite.scale_y = constants.WINDOW_HEIGHT / self.sprite.height
		self.sprite.update(x=constants.WINDOW_WIDTH / 2, y=constants.WINDOW_HEIGHT / 2)

class Button(Node):
	def __init__(self, asset, x, y, unit_width, unit_height, text, on_click, batch, area_group, text_group):
		super().__init__()
		self.text = text
		self.area = Area(asset, x, y, unit_width, unit_height, batch=batch, group=area_group)
		self.on_click = on_click
		self.label = pyglet.text.Label(text, x=x, y=y, anchor_x='center', anchor_y='center', align='center', font_size=15, color=(0, 0, 0, 255), batch=batch, group=text_group)

	def mouse_press_handler(self, command):
		if self.area.within_bounds(command.data['x'], command.data['y']):
			self.on_click()

class TextBox(Area):
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
		self.input_label = pyglet.text.Label(label_text, x=x, y=y + constants.AREA_TILE_SIZE * 2, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(0, 0, 0, 255), batch=batch, group=text_group)
		self.input_error = pyglet.text.Label('', x=x, y=y - 30, anchor_x='left', anchor_y='center', align='left', font_size=15, color=(255, 0, 0, 255), batch=batch, group=text_group)
		self.selected = False

	def set_error_text(self, text):
		self.input_error.text = text

	def get_text(self):
		return self.document.text

	def text_handler(self, command):
		if self.selected:
			self.caret.on_text(command.data['text'])
			self.enforce_length()

	def text_motion_handler(self, command):
		if self.selected:
			self.caret.on_text_motion(command.data['motion'])
			self.enforce_length()

	def text_motion_select_handler(self, command):
		if self.selected:
			self.caret.on_text_motion_select(command.data['motion'])
			self.enforce_length()

	def mouse_press_handler(self, command):
		if self.within_bounds(command.data['x'], command.data['y']):
			self.caret.visible = True
			self.caret.on_mouse_press(command.data['x'], command.data['y'], command.data['button'], command.data['modifiers'])
			self.selected = True
		else:
			self.caret.visible = False
			self.caret.mark = self.caret.position = 0
			self.selected = False

	def mouse_drag_handler(self, command):
		if self.selected:
			self.caret.on_mouse_drag(command.data['x'], command.data['y'], command.data['dx'], command.data['dy'], command.data['buttons'], command.data['modifiers'])
			self.enforce_length()

	def enforce_length(self):
		if len(self.document.text) > self.max_length:
			stored_caret_position = self.caret.position
			self.document.text = self.document.text[:self.max_length]
			self.caret.mark = self.caret.position = stored_caret_position