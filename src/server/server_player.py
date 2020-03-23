from src.shared import attribute_set

class ServerPlayer():
	def __init__(self, name, host, connection=None):
		self.name = name
		self.host = host
		self.connection = connection
		self.game = None
		self.grid_x = None
		self.grid_y = None

	def __eq__(self, obj):
		if self.connection == None:
			return False
		elif isinstance(obj, ServerPlayer):
			return self.connection == obj.connection
		else:
			return self.connection == obj

	def set_character(self, entry):
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
		self.display_name = entry['display_name']
		self.variable_name = entry['variable_name']
		self.related = entry['related']

	def set_position(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y
