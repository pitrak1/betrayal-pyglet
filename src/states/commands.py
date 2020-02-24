class TranslatedMousePress():
	def __init__(self, x, y, button, modifiers):
		self.x = x
		self.y = y
		self.button = button
		self.modifiers = modifiers

class MouseScroll():
	def __init__(self, x, y, dx, dy):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy

class KeyPress():
	def __init__(self, symbol, modifiers):
		self.symbol = symbol
		self.modifiers = modifiers

class MoveCharacter():
	def __init__(self, character, end_x, end_y):
		self.character = character
		self.end_x = end_x
		self.end_y = end_y

class Select():
	def __init__(self, selected):
		self.selected = selected

class PlaceCharacter():
	def __init__(self, character_tile, grid_x, grid_y):
		self.character_tile = character_tile
		self.grid_x = grid_x
		self.grid_y = grid_y

class PlaceRoom():
	def __init__(self, room_tile, grid_x, grid_y, rotation):
		self.room_tile = room_tile
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.rotation = rotation

class GetSelectedCharacterMoveValid():
	def __init__(self, start_x, start_y, end_x, end_y):
		self.start_x = start_x
		self.start_y = start_y
		self.end_x = end_x
		self.end_y = end_y

class GetRoomRotationValid():
	def __init__(self, grid_x, grid_y, entering_direction):
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.entering_direction = entering_direction

class RawMousePress():
	def __init__(self, x, y, button, modifiers):
		self.x = x
		self.y = y
		self.button = button
		self.modifiers = modifiers

class GetCharacterTile():
	def __init__(self, name=None):
		self.name = name

class GetRoomTile():
	def __init__(self, name=None):
		self.name = name

class GetCharacterAsset():
	def __init__(self, asset_name):
		self.asset_name = asset_name

class GetRoomAsset():
	def __init__(self, asset_index):
		self.asset_index = asset_index

class GetMiscAsset():
	def __init__(self, asset_name):
		self.asset_name = asset_name