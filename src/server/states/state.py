from src.shared import node

class State(node.Node):
	def __init__(self, name, players, rooms, set_state, add_command):
		super().__init__()
		self.name = name
		self.players = players
		self.rooms = rooms
		self.set_state = set_state
		self.add_command = add_command