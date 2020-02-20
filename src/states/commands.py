class MousePressCommand():
	def __init__(self, position, button, modifiers):
		self.position = position
		self.button = button
		self.modifiers = modifiers

class KeyPressCommand():
	def __init__(self, symbol, modifiers):
		self.symbol = symbol
		self.modifiers = modifiers

class AddRoomCommand():
	def __init__(self, room_tile, grid_position, rotation):
		self.room_tile = room_tile
		self.grid_position = grid_position
		self.rotation = rotation

class AddCharacterCommand():
	def __init__(self, character_tile, grid_position):
		self.character_tile = character_tile
		self.grid_position = grid_position

class MoveCharacterCommand():
	def __init__(self, character, grid_position):
		self.character = character
		self.grid_position = grid_position