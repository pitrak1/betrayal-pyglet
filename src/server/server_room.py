from src.shared import node as node_module

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class ServerRoom(node_module.Node):
	def __init__(self, entry):
		super().__init__()
		for key, value in entry.items():
			setattr(self, key, value)

		self._players = []
		self.links = []

	def set_position(self, grid_x, grid_y):
		self._grid_x = grid_x
		self._grid_y = grid_y

	def has_door(self, direction):
		return self.doors[direction]

	def add_link(self, room):
		self.links.append(room)

	def has_link(self, room):
		return room in self.links

	def add_player(self, player):
		self._players.append(player)

	def remove_player(self, player):
		print(f'removing {player.name} from {self.display_name}')
		print('Current players:')
		for p in self._players:
			print(p.name)
		self._players.remove(player)
