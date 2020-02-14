class AddCharacterCommand():
	def __init__(self, character_tile, grid_x, grid_y):
		self.character_tile = character_tile
		self.grid_x = grid_x
		self.grid_y = grid_y

class MoveCharacterCommand():
	def __init__(self, character, room):
		self.character = character
		self.room = room

class AddRoomCommand():
	def __init__(self, room_tile, grid_x, grid_y):
		self.room_tile = room_tile
		self.grid_x = grid_x
		self.grid_y = grid_y

class KeyPressCommand():
	def __init__(self, symbol, modifiers):
		self.symbol = symbol
		self.modifiers = modifiers

class MousePressCommand():
	def __init__(self, x, y, button, modifiers):
		self.x = x
		self.y = y
		self.button = button
		self.modifiers = modifiers