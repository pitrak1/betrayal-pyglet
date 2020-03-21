import pyglet
from src.shared import bounds, constants, node, attribute_set

class ClientPlayer(node.Node):
	def __init__(self, entry, asset_manager, name, host, self_, batch, character_group, highlight_group):
		super().__init__()
		self.__asset_manager = asset_manager
		self.__name = name
		self.__host = host
		self.__self_ = self_
		self.__batch = batch
		self.__character_group = character_group
		self.__highlight_group = highlight_group
		self.__display_name = entry['display_name']
		self.__variable_name = entry['variable_name']
		self.__related = entry['related']
		self.__portrait_sprite = pyglet.sprite.Sprite(asset_manager.characters[entry['variable_name']], batch=batch, group=character_group)
		self.__selected_sprite = pyglet.sprite.Sprite(asset_manager.common['character_selected'], batch=batch, group=highlight_group)
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

	def redraw(self):
		self.__portrait_sprite = pyglet.sprite.Sprite(asset_manager.characters[entry['variable_name']], batch=batch, group=character_group)
		if self.__selected:
			self.__selected_sprite = pyglet.sprite.Sprite(asset_manager.common['character_selected'], batch=batch, group=highlight_group)
		


	def client_translated_mouse_press_handler(self, command, state):
		if self.within_bounds(command.data['x'], command.data['y']):
			if command.data['button'] == pyglet.window.mouse.LEFT:
				state.select(self)
				return True
			# elif command.data['button'] == window.mouse.RIGHT and state.name('SelectedState'):
			# 	if not self.default_handler(command, state):
			# 		state.trigger_selected_character_move(self.grid_x, self.grid_y, True)

	def client_select_handler(self, command, state):
		self.selected = command.data['selected'] == self

	def within_bounds(self, x, y):
		return bounds.within_circle_bounds(self.grid_x * constants.GRID_SIZE, self.grid_y * constants.GRID_SIZE, x, y, constants.CHARACTER_SIZE)

