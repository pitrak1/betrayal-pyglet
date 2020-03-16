# # x, y, button, modifiers
	# 'client_raw_mouse_press',

	# # x, y, button, modifiers
	# 'client_translated_mouse_press',

	# # x, y, dx, dy
	# 'client_mouse_scroll',

	# # symbol, modifiers
	# 'client_key_press',

	# # text
	# 'client_text_entered',

	# # character, end_x, end_y
	# 'client_move_character',

	# # selected
	# 'client_select',

	# # character_tile, grid_x, grid_y
	# 'client_place_character',

	# # room_tile, grid_x, grid_y, rotation
	# 'client_place_room',

	# # start_x, start_y, end_x, end_y
	# 'client_get_selected_character_move_valid',

	# # grid_x, grid_y, entering_direction
	# 'client_get_room_rotation_valid',

	# # name
	# 'client_get_character_tile',

	# # name
	# 'client_get_room_tile'

# NETWORK_COMMANDS = [
# 	# status, player_name
# 	'network_create_player',

# 	# status, game_name, password
# 	'network_create_game',

# 	# status
# 	'network_leave_game',

# 	# status
# 	'network_logout',

# 	# status, game_name, players
# 	'network_get_players_in_game',

# 	# status, games
# 	'network_get_games',

# 	# status, game_name, password
# 	'network_join_game',

# 	# status
# 	'network_start_game',

# 	# status, players
# 	'network_get_player_order',

# 	# status
# 	'network_confirm_player_order',

# 	# status, characters
# 	'network_get_available_characters',

# 	# status, player_name
# 	'network_get_current_player',

# 	# status, character
# 	'network_select_character',

# 	# status
# 	'network_all_characters_selected',

# 	# status, selections
# 	'network_get_character_selections',

# 	# status
# 	'network_confirm_character_selections'

	# # players
	# 'network_get_player_positions'
# ]

class Node():
	def __init__(self):
		self.setup_callbacks()

	def setup_callbacks(self):
		self.command_callbacks = {}
		for entry in dir(self):
			if '_handler' in entry:
				self.command_callbacks[entry[:-8]] = getattr(self, entry)

	def on_command(self, command, state=None):
		return self.command_callbacks[command.type](command, state)

	def client_raw_mouse_press_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_translated_mouse_press_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_mouse_scroll_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_key_press_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_text_entered_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_move_character_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_select_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_place_character_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_place_room_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_get_selected_character_move_valid_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_get_room_rotation_valid_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_get_character_tile_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def client_get_room_tile_handler(self, command, state=None):
		return self.default_handler(command, state)

	def server_broadcast_players_handler(self, command, state=None):
		return self.default_handler(command, state)

	def server_destroy_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_create_player_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_create_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_leave_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_get_players_in_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_get_games_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_join_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_logout_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_start_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_get_player_order_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def network_confirm_player_order_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_get_available_characters_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_get_current_player_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_select_character_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	def network_all_characters_selected_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_get_character_selections_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_confirm_character_selections_handler(self, command, state=None):
		return self.default_handler(command, state)

	def network_get_player_positions_handler(self, command, state=None):
		return self.default_handler(command, state)

	def default_handler(self, command, state=None):
		pass

	def on_update(self, dt=None, state=None):
		pass

	def draw(self):
		pass
