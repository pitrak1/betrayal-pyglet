from lattice2d.config import Config
from src.server.server_core import ServerCore
from src.server.server_states import ServerLobbyState

CONFIG = {
	'command_types': [
		'client_select',
		'client_move',
		'network_move',
		'network_start_game',
		'network_get_player_order',
		'network_confirm_player_order',
		'network_get_available_characters',
		'network_get_current_player',
		'network_select_character',
		'network_all_characters_selected',
		'network_get_character_selections',
		'network_confirm_character_selections',
		'network_get_player_positions'
	],
	'log_level': 3,
	'ip_address': '0.0.0.0',
	'port': 8080,
	'full_solution': {
		'network': True,
		'group_count': 6,
		'minimum_players': 1
	}
}

Config(CONFIG)
server = ServerCore()
server.run()