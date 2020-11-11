from lattice2d.grid import Tile, TileGrid, get_direction, get_distance, reverse_direction
from lattice2d.server import Player as Lattice2dPlayer
from constants import Constants


class AttributeSet():
	def __init__(self, speed, speed_index, might, might_index, sanity, sanity_index, knowledge, knowledge_index):
		self.speed = speed
		self.speed_index = speed_index
		self.might = might
		self.might_index = might_index
		self.sanity = sanity
		self.sanity_index = sanity_index
		self.knowledge = knowledge
		self.knowledge_index = knowledge_index

	def get_attribute_value(self, attribute):
		return getattr(self, attribute)[getattr(self, f'{attribute}_index')]

	def change_attribute_value(self, attribute, change):
		setattr(self, f'{attribute}_index', getattr(self, f'{attribute}_index') + change)

		if getattr(self, f'{attribute}_index') < 0: setattr(self, f'{attribute}_index', 0)
		if getattr(self, f'{attribute}_index') > 8: setattr(self, f'{attribute}_index', 8)

	def is_dead(self):
		return self.speed_index == 0 or self.might_index == 0 or self.sanity_index == 0 or self.knowledge_index == 0

class Player(Lattice2dPlayer):
	def __init__(self, name, connection=None, game=None, entry=None, grid_position=(None, None), base_position=(0, 0)):
		super().__init__(name, connection, game)
		self.host = False
		self.attributes = None
		self.display_name = None
		self.variable_name = None
		self.related = None
		if entry:
			self.set_character(entry)
		
	def set_character(self, entry):
		self.entry = entry
		self.attributes = AttributeSet(
			speed=entry['speed'],
			speed_index=entry['speed_index'], 
			might=entry['might'],
			might_index=entry['might_index'], 
			sanity=entry['sanity'], 
			sanity_index=entry['sanity_index'], 
			knowledge=entry['knowledge'], 
			knowledge_index=entry['knowledge_index']
		)
		self.display_name = entry['display_name']
		self.key = entry['key']
		self.related = entry['related']

class ClientPlayer(Player):
	def __init__(self, name, connection=None, game=None, grid_position=(None, None), base_position=(0, 0), add_command=None, character_entry=None):
		super().__init__(name, connection, game, grid_position, base_position, add_command, character_entry)
		self.selected = False

	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.player_sprite = pyglet.sprite.Sprite(
			Assets().characters[self.character_entry['variable_name']],
			x=self.get_scaled_x_position(self.grid_position[0], 0),
			y=self.get_scaled_y_position(self.grid_position[1], 0),
			batch=renderer.get_batch(),
			group=renderer.get_group(2)
		)
		self.player_sprite.update(scale=self.base_scale)
		if self.selected:
			self.player_highlight_sprite = pyglet.sprite.Sprite(
				Assets().custom['character_selected'],
				x=self.get_scaled_x_position(self.grid_position[0], 0),
				y=self.get_scaled_y_position(self.grid_position[1], 0),
				batch=renderer.get_batch(),
				group=renderer.get_group(3)
			)
			self.player_highlight_sprite.update(scale=self.base_scale)

	def mouse_press_handler(self, command):
		if self.within_bounds((command.data['x'], command.data['y'])):
			self.add_command(Command('client_select', { 'selected': self }))
			self.add_command(Command('redraw'))
			return True
		else:
			return False

	def within_bounds(self, position):
		return within_circle_bounds(
			(self.grid_position[0] * Constants.grid_size, self.grid_position[1] * Constants.grid_size), 
			position, 
			Constants.character_size // 2
		)

	def client_select_handler(self, command):
		self.selected = command.data['selected'] == self