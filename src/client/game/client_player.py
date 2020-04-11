import pyglet
from src.common import bounds, constants, node, attribute_set, logger

class ClientPlayer(node.Node):
	def __init__(self, entry, name, host, self_, testing=False):
		super().__init__()
		self.entry = entry
		self.display_name = entry['display_name']
		self.variable_name = entry['variable_name']
		self.related = entry['related']
		self.selected = False
		self.testing = testing
		self.attributes = attribute_set.AttributeSet(
			speed=entry['speed'],
			speed_index=entry['speed_index'], 
			might=entry['might'],
			might_index=entry['might_index'], 
			sanity=entry['sanity'], 
			sanity_index=entry['sanity_index'], 
			knowledge=entry['knowledge'], 
			knowledge_index=entry['knowledge_index']
		)
		self.name = name
		self.host = host
		self.self_ = self_
		self.grid_x = None
		self.grid_y = None
		self.x = None
		self.y = None
		self.scale = 1

	def redraw(self, command, state):
		if not self.testing:
			self.portrait_sprite = pyglet.sprite.Sprite(
				command.data['asset_manager'].characters[self.variable_name],
				x=self.x,
				y=self.y,
				batch=command.data['batch'],
				group=command.data['groups'][constants.CHARACTERS_AND_DOORS_GROUP]
			)
			if self.selected:
				self.selected_sprite = pyglet.sprite.Sprite(
					command.data['asset_manager'].common['character_selected'], 
					x=self.x,
					y=self.y,
					batch=command.data['batch'], 
					group=command.data['groups'][constants.HIGHLIGHTS_GROUP]
				)


	def client_redraw_handler(self, command, state=None):
		logger.log(f'Player {self.variable_name} handling command', logger.LOG_LEVEL_COMMAND)
		self.redraw(command, state)

	def set_position(self, grid_x, grid_y, x, y, scale):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.x = x
		self.y = y
		self.scale = scale

	def client_mouse_press_handler(self, command, state):
		logger.log(f'Player {self.variable_name} handling command', logger.LOG_LEVEL_COMMAND)
		if self.within_bounds(command.data['x'], command.data['y']):
			logger.log(f'Within bounds of Player {self.variable_name}', logger.LOG_LEVEL_DEBUG)
			if command.data['button'] == pyglet.window.mouse.LEFT:
				logger.log(f'LMB within bounds of Player {self.variable_name}, selecting', logger.LOG_LEVEL_DEBUG)
				state.select(self)
				return True

	def client_select_handler(self, command, state):
		logger.log(f'Player {self.variable_name} handling command', logger.LOG_LEVEL_COMMAND)
		self.selected = command.data['selected'] == self

	def within_bounds(self, x, y):
		return bounds.within_circle_bounds(self.x, self.y, x, y, constants.CHARACTER_SIZE // 2)

