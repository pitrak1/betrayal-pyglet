import os
import definitions
from src.client.menu_states import SplashState, CreatePlayerState, MainMenuState, CreateGameState, GameListState, LobbyState as ClientLobbyState
from src.client.setup_states import PlayerOrderState, CharacterSelectionState, CharacterOverviewState
from src.client.game_states import BaseState
from src.server.states import SetupState, LobbyState as ServerLobbyState, GameState
from src.common.player import Player
from src.common.grid import Room
from constants import Constants


CONFIG = {
	'window_dimensions': Constants.window_dimensions,
	'network': {
		'ip_address': '0.0.0.0',
		'port': 8080
	},
	'logging': {
		'lattice2d_core': 'cyan',
		# 'lattice2d_network': 'red',
		# 'lattice2d_components': 'yellow',
		# 'lattice2d_rendering': 'green'
	},
	'rendering': {
		'layers': ['background', 'base', 'environment', 'actors', 'ui'],
		'groups_per_layer': 2
	},
	'grid': {
		'width': Constants.grid_dimensions_x,
		'height': Constants.grid_dimensions_y,
		'size': Constants.grid_size
	},
	'command_types': [
		'client_select',
		'client_move',
		'network_move',
		'start_game',
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
	'empty_tile_class': Room,
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
		'path': os.path.join(definitions.ROOT_DIR, 'assets'),
		'resources': [
			{
				'key': 'rooms',
				'location': 'rooms.jpg',
				'type': 'grid',
				'rows': 9,
				'columns': 8,
				'resources': [
					{
						'key': 'dungeon',
						'index': 8
					},
					{
						'key': 'entrance_hall',
						'index': 2
					},
					{
						'key': 'foyer',
						'index': 1
					},
					{
						'key': 'grand_staircase',
						'index': 0
					}
				]
			},
			{
				'key': 'heather_granville',
				'location': 'heather_granville.png',
				'type': 'single'
			},
			{
				'key': 'jenny_leclerc',
				'location': 'jenny_leclerc.png',
				'type': 'single'
			},
			{
				'key': 'madame_zostra',
				'location': 'madame_zostra.png',
				'type': 'single'
			},
			{
				'key': 'vivian_lopez',
				'location': 'vivian_lopez.png',
				'type': 'single'
			},
			{
				'key': 'brandon_jaspers',
				'location': 'brandon_jaspers.png',
				'type': 'single'
			},
			{
				'key': 'peter_akimoto',
				'location': 'peter_akimoto.png',
				'type': 'single'
			},
			{
				'key': 'darrin_williams',
				'location': 'darrin_williams.png',
				'type': 'single'
			},
			{
				'key': 'ox_bellows',
				'location': 'ox_bellows.png',
				'type': 'single'
			},
			{
				'key': 'zoe_ingstrom',
				'location': 'zoe_ingstrom.png',
				'type': 'single'
			},
			{
				'key': 'missy_dubourde',
				'location': 'missy_dubourde.png',
				'type': 'single'
			},
			{
				'key': 'professor_longfellow',
				'display_name': 'Professor Longfellow',
				'location': 'professor_longfellow.png',
				'type': 'single'
			},
			{
				'key': 'father_rhinehardt',
				'location': 'father_rhinehardt.png',
				'type': 'single'
			},
			{
				'key': 'menu_background',
				'location': 'menu_background.jpg',
				'type': 'single'
			},
			{
				'key': 'host_marker',
				'location': 'crown.png',
				'type': 'single'
			},
			{
				'key': 'attribute_highlight',
				'location': 'attribute_highlight.png',
				'type': 'single'
			},
			{
				'key': 'character_selected',
				'location': 'character_selected.png',
				'type': 'single'
			},
			{
				'key': 'door',
				'location': 'door.png',
				'type': 'single'
			},
			{
				'key': 'room_selected',
				'location': 'room_selected.png',
				'type': 'single'
			},
			{
				'key': 'grey_panel',
				'location': 'grey_panel.png',
				'type': 'grid',
				'rows': 3,
				'columns': 3
			},
			{
				'key': 'grey_button',
				'location': 'grey_button.png',
				'type': 'grid',
				'rows': 3,
				'columns': 3
			}
		]
	}
}
