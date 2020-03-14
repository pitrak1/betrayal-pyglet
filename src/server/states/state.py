from src.shared import node

class State(node.Node):
	def __init__(self, data, set_state, add_command):
		super().__init__()
		self.players = data['players']
		self.rooms = data['rooms']
		self.set_state = set_state
		self.add_command = add_command