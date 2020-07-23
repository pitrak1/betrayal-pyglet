import os
import definitions
from src.client.menu_states.splash_state import SplashState
from src.client.menu_states.create_player_state import CreatePlayerState
from src.client.menu_states.main_menu_state import MainMenuState
from src.client.menu_states.create_game_state import CreateGameState
from src.client.menu_states.game_list_state import GameListState
from src.client.menu_states.lobby_state import LobbyState as ClientLobbyState
from src.client.setup_states.player_order_state import PlayerOrderState
from src.client.setup_states.character_selection_state import CharacterSelectionState
from src.client.setup_states.character_overview_state import CharacterOverviewState
from src.server.setup_state import SetupState
from src.server.lobby_state import LobbyState as ServerLobbyState

CONFIG = {
	'window_dimensions': (1280, 720),
	'log_level': 3,
	'network': {
		'ip_address': '0.0.0.0',
		'port': 8080
	},
	'group_count': 6,
	'grid': {
		'width': 10,
		'height': 10,
		'size': 512
	},
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
	'client_states': {
		'starting_state': SplashState,
		'states': [
			{
				'state': SplashState,
				'transitions': {
					'to_create_player_state': CreatePlayerState
				}
			},
			{
				'state': CreatePlayerState,
				'transitions': {
					'to_main_menu_state': MainMenuState
				}
			},
			{
				'state': MainMenuState,
				'transitions': {
					'to_create_game_state': CreateGameState,
					'to_join_game_state': GameListState
				}
			},
			{
				'state': CreateGameState,
				'transitions': {
					'to_main_menu_state': MainMenuState,
					'to_lobby_state': ClientLobbyState
				}
			},
			{
				'state': GameListState,
				'transitions': {
					'to_main_menu_state': MainMenuState,
					'to_lobby_state': ClientLobbyState
				}
			},
			{
				'state': ClientLobbyState,
				'transitions': {
					'to_main_menu_state': MainMenuState,
					'to_player_order_state': PlayerOrderState
				}
			},
			{
				'state': PlayerOrderState,
				'transitions': {
					'to_character_selection_state': CharacterSelectionState
				}
			},
			{
				'state': CharacterSelectionState,
				'transitions': {
					'to_character_overview_state': CharacterOverviewState
				}
			},
			{
				'state': CharacterOverviewState,
				'transitions': {}
			}
		]
	},
	'server_states': {
		'starting_state': ServerLobbyState,
		'states': [
			{
				'state': ServerLobbyState,
				'transitions': {
					'to_setup_state': SetupState
				}
			},
			{
				'state': SetupState,
				'transitions': {}
			}
		]
	},
	'assets': {
		'path': os.path.join(definitions.ROOT_DIR,'assets'),
		'tiles': [
			{
				'display_name': 'Dungeon',
				'variable_name': 'dungeon',
				'asset': {
					'location': 'rooms.jpg',
					'type': 'grid',
					'index': 8
				}
			}
		],
		'characters': {
			'heather_granville': {
				'display_name': 'Heather Granville',
				'location': 'heather_granville.png',
				'type': 'single',
				'speed': [0, 3, 3, 4, 5, 6, 6, 7, 8],
				'speed_index': 3,
				'might': [0, 3, 3, 3, 4, 5, 6, 7, 8],
				'might_index': 3,
				'sanity': [0, 3, 3, 3, 4, 5, 6, 6, 6],
				'sanity_index': 3,
				'knowledge': [0, 2, 3, 3, 4, 5, 6, 7, 8],
				'knowledge_index': 5,
				'related': ['jenny_leclerc']
			},
			'jenny_leclerc': {
				'display_name': 'Jenny LeClerc',
				'location': 'jenny_leclerc.png',
				'type': 'single',
				'speed': [0, 2, 3, 4, 4, 4, 5, 6, 8],
				'speed_index': 4,
				'might': [0, 3, 4, 4, 4, 4, 5, 6, 8],
				'might_index': 3,
				'sanity': [0, 1, 1, 2, 4, 4, 4, 5, 6],
				'sanity_index': 5,
				'knowledge': [0, 2, 3, 3, 4, 4, 5, 6, 8],
				'knowledge_index': 3,
				'related': ['heather_granville']
			},
			'madame_zostra': {
				'display_name': 'Madame Zostra',
				'location': 'madame_zostra.png',
				'type': 'single',
				'speed': [0, 2, 3, 3, 5, 5, 6, 6, 7],
				'speed_index': 3,
				'might': [0, 2, 3, 3, 4, 5, 5, 5, 6],
				'might_index': 4,
				'sanity': [0, 4, 4, 4, 5, 6, 7, 8, 8],
				'sanity_index': 3,
				'knowledge': [0, 1, 3, 4, 4, 4, 5, 6, 6],
				'knowledge_index': 4,
				'related': ['vivian_lopez']
			},
			'vivian_lopez': {
				'display_name': 'Vivian Lopez',
				'location': 'vivian_lopez.png',
				'type': 'single',
				'speed': [0, 3, 4, 4, 4, 4, 6, 7, 8],
				'speed_index': 4,
				'might': [0, 2, 2, 2, 4, 4, 5, 6, 6],
				'might_index': 3,
				'sanity': [0, 4, 4, 4, 5, 6, 7, 8, 8],
				'sanity_index': 3,
				'knowledge': [0, 4, 5, 5, 5, 5, 6, 6, 7],
				'knowledge_index': 4,
				'related': ['madame_zostra']
			},
			'brandon_jaspers': {
				'display_name': 'Brandon Jaspers',
				'location': 'brandon_jaspers.png',
				'type': 'single',
				'speed': [0, 3, 4, 4, 4, 5, 6, 7, 8],
				'speed_index': 3,
				'might': [0, 2, 3, 3, 4, 5, 6, 6, 7],
				'might_index': 4,
				'sanity': [0, 3, 3, 3, 4, 5, 6, 7, 8],
				'sanity_index': 4,
				'knowledge': [0, 1, 3, 3, 5, 5, 6, 6, 7],
				'knowledge_index': 3,
				'related': ['peter_akimoto']
			},
			'peter_akimoto': {
				'display_name': 'Peter Akimoto',
				'location': 'peter_akimoto.png',
				'type': 'single',
				'speed': [0, 3, 3, 3, 4, 6, 6, 7, 7],
				'speed_index': 4,
				'might': [0, 2, 3, 3, 4, 5, 5, 6, 8],
				'might_index': 3,
				'sanity': [0, 3, 4, 4, 4, 5, 6, 6, 7],
				'sanity_index': 4,
				'knowledge': [0, 3, 4, 4, 5, 6, 7, 7, 8],
				'knowledge_index': 3,
				'related': ['brandon_jaspers']
			},
			'darrin_williams': {
				'display_name': 'Darrin Williams',
				'location': 'darrin_williams.png',
				'type': 'single',
				'speed': [0, 4, 4, 4, 5, 6, 7, 7, 8],
				'speed_index': 5,
				'might': [0, 2, 3, 3, 4, 5, 6, 6, 7],
				'might_index': 3,
				'sanity': [0, 1, 2, 3, 4, 5, 5, 5, 7],
				'sanity_index': 3,
				'knowledge': [0, 2, 3, 3, 4, 5, 5, 5, 7],
				'knowledge_index': 3,
				'related': ['ox_bellows']
			},
			'ox_bellows': {
				'display_name': 'Ox Bellows',
				'location': 'ox_bellows.png',
				'type': 'single',
				'speed': [0, 2, 2, 2, 3, 4, 5, 5, 6],
				'speed_index': 5,
				'might': [0, 4, 5, 5, 6, 6, 7, 8, 8],
				'might_index': 3,
				'sanity': [0, 2, 2, 3, 4, 5, 5, 6, 7],
				'sanity_index': 3,
				'knowledge': [0, 2, 2, 3, 3, 5, 5, 6, 6],
				'knowledge_index': 3,
				'related': ['darrin_williams']
			},
			'zoe_ingstrom': {
				'display_name': 'Zoe Ingstrom',
				'location': 'zoe_ingstrom.png',
				'type': 'single',
				'speed': [0, 4, 4, 4, 4, 5, 6, 8, 8],
				'speed_index': 4,
				'might': [0, 2, 2, 3, 3, 4, 4, 6, 7],
				'might_index': 4,
				'sanity': [0, 3, 4, 5, 5, 6, 6, 7, 8],
				'sanity_index': 3,
				'knowledge': [0, 1, 2, 3, 4, 4, 5, 5, 5],
				'knowledge_index': 3,
				'related': ['missy_dubourde']
			},
			'missy_dubourde': {
				'display_name': 'Missy Dubourde',
				'location': 'missy_dubourde.png',
				'type': 'single',
				'speed': [0, 3, 4, 5, 6, 6, 6, 7, 7],
				'speed_index': 3,
				'might': [0, 2, 3, 3, 3, 4, 5, 6, 7],
				'might_index': 4,
				'sanity': [0, 1, 2, 3, 4, 5, 5, 6, 7],
				'sanity_index': 3,
				'knowledge': [0, 2, 3, 4, 4, 5, 6, 6, 6],
				'knowledge_index': 4,
				'related': ['zoe_ingstrom']
			},
			'professor_longfellow': {
				'display_name': 'Professor Longfellow',
				'location': 'professor_longfellow.png',
				'type': 'single',
				'speed': [0, 2, 2, 4, 4, 5, 5, 6, 6],
				'speed_index': 4,
				'might': [0, 1, 2, 3, 4, 5, 5, 6, 6],
				'might_index': 3,
				'sanity': [0, 1, 3, 3, 4, 5, 5, 6, 7],
				'sanity_index': 3,
				'knowledge': [0, 4, 5, 5, 5, 5, 6, 7, 8],
				'knowledge_index': 5,
				'related': ['father_rhinehardt']
			},
			'father_rhinehardt': {
				'display_name': 'Father Rhinehardt',
				'location': 'father_rhinehardt.png',
				'type': 'single',
				'speed': [0, 2, 3, 3, 4, 5, 6, 7, 7],
				'speed_index': 3,
				'might': [0, 1, 2, 2, 4, 4, 5, 5, 7],
				'might_index': 3,
				'sanity': [0, 3, 4, 5, 5, 6, 7, 7, 8],
				'sanity_index': 5,
				'knowledge': [0, 1, 3, 3, 4, 5, 6, 6, 8],
				'knowledge_index': 4,
				'related': ['professor_longfellow']
			}
		},
		'custom': {
			'menu_background': {
				'location': 'menu_background.jpg',
				'type': 'single'
			},
			'host_marker': {
				'location': 'crown.png',
				'type': 'single'
			},
			'attribute_highlight': {
				'location': 'attribute_highlight.png',
				'type': 'single'
			},
			'host_marker': {
				'location': 'crown.png',
				'type': 'single'
			}
		}
	}
}