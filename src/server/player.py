class Player():
	def __init__(self, name, host, connection=None):
		self.name = name
		self.host = host
		self.connection = connection
		self.game = None
		self.character = None
		self.grid_x = None
		self.grid_y = None

	def __eq__(self, obj):
		if self.connection == None:
			return False
		elif isinstance(obj, Player):
			return self.connection == obj.connection
		else:
			return self.connection == obj
