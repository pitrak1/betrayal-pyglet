from src.common.attribute_set import AttributeSet
from lattice2d.grid import Actor, Tile, TileGrid, get_direction, reverse_direction
from lattice2d.full.full_server import FullServerPlayer
from src.common import constants
import config

class ServerPlayer(FullServerPlayer):
	def __init__(self, name, connection, game=None):
		super().__init__(name, connection, game)
		self.host = False
		self.attributes = None
		self.display_name = None
		self.variable_name = None
		self.related = None
		
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

class ServerRoom(Tile):
	def __init__(self, entry):
		super().__init__(entry['grid_x'], entry['grid_y'])
		self.entry = entry
		self.display_name = entry['display_name']
		self.variable_name = entry['variable_name']
		self.asset_index = entry['asset_index']
		self.doors = entry['doors']
		self.floor = entry['floor']
		self.sprite_rotation = entry['sprite_rotation']
		self.players = []
		self.links = []

class ServerRoomGrid(TileGrid):
	def __init__(self):
		super().__init__(constants.GRID_WIDTH, constants.GRID_HEIGHT)
		for room in config.STARTING_ROOMS:
			self.add_tile(room['grid_x'], room['grid_y'], ServerRoom(room))

	def add_adjacent_links(self, start_tile, end_tile):
		if isinstance(end_tile, Tile):
			direction = get_direction(start_tile.grid_x, start_tile.grid_y, end_tile.grid_x, end_tile.grid_y)
			if start_tile.doors[direction] and end_tile.doors[reverse_direction(direction)]:
				start_tile.links.append(end_tile)
				end_tile.links.append(start_tile)
