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
from src.client.game_states.base_state import BaseState
from src.server.setup_state import SetupState
from src.server.lobby_state import LobbyState as ServerLobbyState
from src.server.game_state import GameState
from src.common.player import Player

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
	'player_class': Player,
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
				'transitions': {
					'to_game_base_state': BaseState
				}
			},
			{
				'state': BaseState,
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
				'transitions': {
					'to_game_state': GameState
				}
			},
			{
				'state': GameState,
				'transitions': {}
			}
		]
	},
	'assets': {
		'path': os.path.join(definitions.ROOT_DIR,'assets'),
		'tiles': [
			{
				'location': 'rooms.jpg',
				'type': 'grid',
				'rows': 9,
				'columns': 8,
				'assets': [
					{
						'variable_name': 'dungeon',
						'index': 8
					},
					{
						'variable_name': 'entrance_hall',
						'index': 2
					},
					{
						'variable_name': 'foyer',
						'index': 1
					},
					{
						'variable_name': 'grand_staircase',
						'index': 0
					}
				]
			}
		],
		'characters': [
			{
				'variable_name': 'heather_granville',
				'display_name': 'Heather Granville',
				'location': 'heather_granville.png',
				'type': 'single'
			},
			{
				'variable_name': 'jenny_leclerc',
				'display_name': 'Jenny LeClerc',
				'location': 'jenny_leclerc.png',
				'type': 'single'
			},
			{
				'variable_name': 'madame_zostra',
				'display_name': 'Madame Zostra',
				'location': 'madame_zostra.png',
				'type': 'single'
			},
			{
				'variable_name': 'vivian_lopez',
				'display_name': 'Vivian Lopez',
				'location': 'vivian_lopez.png',
				'type': 'single'
			},
			{
				'variable_name': 'brandon_jaspers',
				'display_name': 'Brandon Jaspers',
				'location': 'brandon_jaspers.png',
				'type': 'single'
			},
			{
				'variable_name': 'peter_akimoto',
				'display_name': 'Peter Akimoto',
				'location': 'peter_akimoto.png',
				'type': 'single'
			},
			{
				'variable_name': 'darrin_williams',
				'display_name': 'Darrin Williams',
				'location': 'darrin_williams.png',
				'type': 'single'
			},
			{
				'variable_name': 'ox_bellows',
				'display_name': 'Ox Bellows',
				'location': 'ox_bellows.png',
				'type': 'single'
			},
			{
				'variable_name': 'zoe_ingstrom',
				'display_name': 'Zoe Ingstrom',
				'location': 'zoe_ingstrom.png',
				'type': 'single'
			},
			{
				'variable_name': 'missy_dubourde',
				'display_name': 'Missy Dubourde',
				'location': 'missy_dubourde.png',
				'type': 'single'
			},
			{
				'variable_name': 'professor_longfellow',
				'display_name': 'Professor Longfellow',
				'location': 'professor_longfellow.png',
				'type': 'single'
			},
			{
				'variable_name': 'father_rhinehardt',
				'display_name': 'Father Rhinehardt',
				'location': 'father_rhinehardt.png',
				'type': 'single'
			}
		],
		'custom': [
			{
				'variable_name': 'menu_background',
				'location': 'menu_background.jpg',
				'type': 'single'
			},
			{
				'variable_name': 'host_marker',
				'location': 'crown.png',
				'type': 'single'
			},
			{
				'variable_name': 'attribute_highlight',
				'location': 'attribute_highlight.png',
				'type': 'single'
			},
			{
				'variable_name': 'character_selected',
				'location': 'character_selected.png',
				'type': 'single'
			},
			{
				'variable_name': 'door',
				'location': 'door.png',
				'type': 'single'
			},
			{
				'variable_name': 'room_selected',
				'location': 'room_selected.png',
				'type': 'single'
			}
		]
	}
}