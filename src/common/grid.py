from lattice2d.full.common import FullPlayer, FullPlayerList
from lattice2d.grid import Tile, ScaledTile, ScaledTileGrid, get_direction, get_distance, reverse_direction
from src.common import constants

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

class Player(FullPlayer):
	def __init__(self, name, connection=None, game=None, entry=None):
		super().__init__(name, connection, game)
		self.host = False
		self.attributes = None
		self.display_name = None
		self.variable_name = None
		self.related = None
		if entry:
			self.set_character(entry)
		
	def set_character(self, entry):
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
		self.variable_name = entry['variable_name']
		self.related = entry['related']

class Room(ScaledTile):
	def __init__(self, entry, base_x=0, base_y=0):
		super().__init__(entry['grid_x'], entry['grid_y'], base_x, base_y)
		self.entry = entry
		self.display_name = entry['display_name']
		self.variable_name = entry['variable_name']
		self.asset_index = entry['asset_index']
		self.doors = entry['doors']
		self.floor = entry['floor']
		self.sprite_rotation = entry['sprite_rotation']
		self.players = FullPlayerList()
		self.links = []

class RoomGrid(ScaledTileGrid):
	def __init__(self):
		super().__init__(constants.GRID_WIDTH, constants.GRID_HEIGHT, constants.WINDOW_CENTER_X, constants.WINDOW_CENTER_Y)

	def add_adjacent_links(self, start_tile, end_tile):
		if isinstance(end_tile, Tile):
			direction = get_direction(start_tile.grid_x, start_tile.grid_y, end_tile.grid_x, end_tile.grid_y)
			if start_tile.doors[direction] and end_tile.doors[reverse_direction(direction)]:
				start_tile.links.append(end_tile)
				end_tile.links.append(start_tile)