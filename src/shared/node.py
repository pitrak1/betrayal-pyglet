class Node():
	def __init__(self):
		self.setup_callbacks()

	def setup_callbacks(self):
		self.__command_callbacks = {}
		for entry in dir(self):
			if '_handler' in entry:
				self.__command_callbacks[entry[:-8]] = getattr(self, entry)

	def on_command(self, command, state=None):
		return self.__command_callbacks[command.type](command, state)

	# x, y, button, modifiers
	def client_raw_mouse_press_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	# x, y, button, modifiers
	def client_translated_mouse_press_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	# x, y, dx, dy
	def client_mouse_scroll_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	# symbol, modifiers
	def client_key_press_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	# text
	def client_text_entered_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	# selected
	def client_select_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	# exception
	def server_broadcast_players_handler(self, command, state=None):
		return self.default_handler(command, state)

	# game_name
	def server_destroy_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, player_name
	def network_create_player_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, game_name, password
	def network_create_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status
	def network_leave_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, game_name, players
	def network_get_players_in_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, games
	def network_get_games_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, game_name, password
	def network_join_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status
	def network_logout_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status
	def network_start_game_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, players
	def network_get_player_order_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	# status
	def network_confirm_player_order_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, characters
	def network_get_available_characters_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, player_name
	def network_get_current_player_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, character
	def network_select_character_handler(self, command, state=None):
		return self.default_handler(command, state)
		
	# status
	def network_all_characters_selected_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, selections
	def network_get_character_selections_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status
	def network_confirm_character_selections_handler(self, command, state=None):
		return self.default_handler(command, state)

	# status, players
	def network_get_player_positions_handler(self, command, state=None):
		return self.default_handler(command, state)

	def default_handler(self, command, state=None):
		pass

	def on_update(self, dt=None, state=None):
		pass

	def draw(self):
		pass
