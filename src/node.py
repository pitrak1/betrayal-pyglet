from src.states import commands as commands_module

class Node():
	def on_draw(self, state):
		raise NotImplementedError('on_draw must be overridden')

	def on_command(self, command, state):	
		if isinstance(command, commands_module.RawMousePress):
			return self.raw_mouse_press_handler(command, state)
		elif isinstance(command, commands_module.TranslatedMousePress):
			return self.translated_mouse_press_handler(command, state)
		elif isinstance(command, commands_module.MouseScroll):
			return self.mouse_scroll_handler(command, state)
		elif isinstance(command, commands_module.KeyPress):
			return self.key_press_handler(command, state)
		elif isinstance(command, commands_module.MoveCharacter):
			return self.move_character_handler(command, state)
		elif isinstance(command, commands_module.Select):
			return self.select_handler(command, state)
		elif isinstance(command, commands_module.PlaceCharacter):
			return self.place_character_handler(command, state)
		elif isinstance(command, commands_module.PlaceRoom):
			return self.place_room_handler(command, state)
		elif isinstance(command, commands_module.GetSelectedCharacterMoveValid):
			return self.get_selected_character_move_valid_handler(command, state)
		elif isinstance(command, commands_module.GetRoomRotationValid):
			return self.get_room_rotation_valid_handler(command, state)
		elif isinstance(command, commands_module.GetCharacterTile):
			return self.get_character_tile_handler(command, state)
		elif isinstance(command, commands_module.GetRoomTile):
			return self.get_room_tile_handler(command, state)
		elif isinstance(command, commands_module.GetCharacterAsset):
			return self.get_character_asset_handler(command, state)
		elif isinstance(command, commands_module.GetRoomAsset):
			return self.get_room_asset_handler(command, state)
		elif isinstance(command, commands_module.GetMiscAsset):
			return self.get_misc_asset_handler(command, state)

	def raw_mouse_press_handler(self, command, state):
		self.default_handler(command, state)

	def translated_mouse_press_handler(self, command, state):
		self.default_handler(command, state)

	def mouse_scroll_handler(self, command, state):
		self.default_handler(command, state)

	def key_press_handler(self, command, state):
		self.default_handler(command, state)

	def move_character_handler(self, command, state):
		self.default_handler(command, state)

	def select_handler(self, command, state):
		self.default_handler(command, state)

	def place_character_handler(self, command, state):
		self.default_handler(command, state)

	def place_room_handler(self, command, state):
		self.default_handler(command, state)

	def get_selected_character_move_valid_handler(self, command, state):
		self.default_handler(command, state)

	def get_room_rotation_valid_handler(self, command, state):
		self.default_handler(command, state)

	def get_character_tile_handler(self, command, state):
		self.default_handler(command, state)

	def get_room_tile_handler(self, command, state):
		self.default_handler(command, state)

	def get_character_asset_handler(self, command, state):
		self.default_handler(command, state)

	def get_room_asset_handler(self, command, state):
		self.default_handler(command, state)

	def get_misc_asset_handler(self, command, state):
		self.default_handler(command, state)

	def default_handler(self, command, state):
		raise NotImplementedError('default_handler must be overridden')

	def on_update(self, dt, state):
		raise NotImplementedError('on_update must be overridden')
