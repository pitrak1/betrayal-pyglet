import pyglet
from src.shared import bounds, constants, node, attribute_set

class ClientPlayer(node.Node):
	def __init__(self, entry, name, host, self_):
		super().__init__()
		self.__display_name = entry['display_name']
		self.__variable_name = entry['variable_name']
		self.__related = entry['related']
		self.__selected = False
		self.__attributes = attribute_set.AttributeSet(
			speed=entry['speed'],
			speed_index=entry['speed_index'], 
			might=entry['might'],
			might_index=entry['might_index'], 
			sanity=entry['sanity'], 
			sanity_index=entry['sanity_index'], 
			knowledge=entry['knowledge'], 
			knowledge_index=entry['knowledge_index']
		)
		self.__name = name
		self.__host = host
		self.__self_ = self_
		self.__grid_x = None
		self.__grid_y = None
		self.__x = None
		self.__y = None
		self.__scale = 1

	def client_redraw_handler(self, command, state=None):
		self.__portrait_sprite = pyglet.sprite.Sprite(
			command.data['asset_manager'].characters[self.__variable_name],
			x=self.__x,
			y=self.__y,
			batch=command.data['batch'],
			group=command.data['groups'][constants.CHARACTERS_AND_DOORS_GROUP]
		)
		if self.__selected:
			self.__selected_sprite = pyglet.sprite.Sprite(
				command.data['asset_manager'].common['character_selected'], 
				x=self.__x,
				y=self.__y,
				batch=command.data['batch'], 
				group=command.data['groups'][constants.HIGHLIGHTS_GROUP]
			)

	def set_position(self, grid_x, grid_y, x, y, scale):
		self.__grid_x = grid_x
		self.__grid_y = grid_y
		self.__x = x
		self.__y = y
		self.__scale = scale

	def client_translated_mouse_press_handler(self, command, state):
		if self.within_bounds(command.data['x'], command.data['y']):
			if command.data['button'] == pyglet.window.mouse.LEFT:
				state.select(self)
				return True
			# elif command.data['button'] == window.mouse.RIGHT and state.name('SelectedState'):
			# 	if not self.default_handler(command, state):
			# 		state.trigger_selected_character_move(self.grid_x, self.grid_y, True)

	def client_select_handler(self, command, state):
		self.__selected = command.data['selected'] == self

	def within_bounds(self, x, y):
		return bounds.within_circle_bounds(self.__x, self.__y, x, y, constants.CHARACTER_SIZE // 2)

