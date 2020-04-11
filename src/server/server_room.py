from src.common import node as node_module

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class ServerRoom(node_module.Node):
	def __init__(self, entry):
		super().__init__()
		self.entry = entry
		self.display_name = entry['display_name']
		self.variable_name = entry['variable_name']
		self.asset_index = entry['asset_index']
		self.doors = entry['doors']
		self.floor = entry['floor']
		self.grid_x = entry['grid_x']
		self.grid_y = entry['grid_y']
		self.sprite_rotation = entry['sprite_rotation']
		self.players = []
		self.links = []

	def set_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y

	def has_door(self, direction):
		return self.doors[direction]

	def add_link(self, room):
		self.links.append(room)

	def has_link(self, room):
		return room in self.links

	def add_player(self, player):
		self.players.append(player)

	def remove_player(self, player):
		self.players.remove(player)
