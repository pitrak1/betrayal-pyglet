import pytest
import pyglet
from src.server.states import server_character_selection_state
from src.common import command
import types
import random
import config

class TestServerCharacterSelectionState():
	class TestGetPlayerOrderHandler():
		def test_sends_command(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('get_player_order', { 'status': 'pending', 'players': [] })
			state.network_get_player_order_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'players': ['player0', 'player1'] })

	class TestConfirmPlayerOrderHandler():
		def test_does_not_send_command_if_less_than_number_of_players(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_confirm_player_order', { 'status': 'pending' })
			state.network_confirm_player_order_handler(command_)
			command.update_and_send_to_all.assert_not_called()

		def test_sends_command_if_equal_to_number_of_players(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_confirm_player_order', { 'status': 'pending' })
			state.network_confirm_player_order_handler(command_)
			state.network_confirm_player_order_handler(command_)
			command.update_and_send_to_all.assert_called_once_with(command_, { 'status': 'success' }, state.game.players)

	class TestGetAvailableCharactersHandler():
		def test_sends_command(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_available_characters', { 'status': 'pending' })
			state.network_get_available_characters_handler(command_)
			characters = [c['variable_name'] for c in config.CHARACTERS]
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'characters': characters })

	class TestGetCurrentPlayerHandler():
		def test_sends_command_with_self_if_current_player(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_current_player', { 'status': 'pending', 'connection': 'player1_connection' })
			state.network_get_current_player_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'player_name': 'self' })

		def test_sends_command_with_player_name_if_not_current_player(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_current_player', { 'status': 'pending', 'connection': 'player0_connection' })
			state.network_get_current_player_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'player_name': 'player1' })

	class TestNetworkSelectCharacterHandler():
		def test_sets_character_for_player(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_select_character_handler', { 'status': 'pending', 'connection': 'player1_connection', 'character': config.CHARACTERS[0]['variable_name'] })
			state.network_select_character_handler(command_)
			player = next(p for p in state.game.players if p.name == 'player1')
			player.set_character.assert_called_once_with(config.CHARACTERS[0])

		def test_removes_character(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_select_character_handler', { 'status': 'pending', 'connection': 'player1_connection', 'character': config.CHARACTERS[0]['variable_name'] })
			state.network_select_character_handler(command_)
			assert len([c for c in state.characters if c == config.CHARACTERS[0]['variable_name']]) == 0

		def test_sends_network_all_characters_selected_command_if_last_player(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_select_character_handler', { 'status': 'pending', 'connection': 'player0_connection', 'character': config.CHARACTERS[0]['variable_name'] })
			state.current_player_index = 0
			state.network_select_character_handler(command_)
			command.create_and_send_to_all.assert_called_once_with('network_all_characters_selected', { 'status': 'success' }, state.game.players)

		def test_sends_network_get_current_player_command_if_not_last_player(self, mocker, create_game, get_args):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_select_character_handler', { 'status': 'pending', 'connection': 'player1_connection', 'character': config.CHARACTERS[0]['variable_name'] })
			state.network_select_character_handler(command_)
			assert get_args(command.create_and_send_to_all, 0) == ('network_get_current_player', { 'status': 'success', 'player_name': 'player0' }, state.game.players)

		def test_sends_network_get_available_characters_command_if_not_last_player(self, mocker, create_game, get_args):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_available_characters', { 'status': 'pending', 'connection': 'player1_connection', 'character': config.CHARACTERS[0]['variable_name'] })
			state.network_select_character_handler(command_)
			assert get_args(command.create_and_send_to_all, 1) == (
				'network_get_available_characters', 
				{ 
					'status': 'success', 
					'characters': [c['variable_name'] for c in config.CHARACTERS if c != config.CHARACTERS[0] and c != config.CHARACTERS[1]] 
				}, 
				state.game.players
			)

	class TestNetworkGetCharacterSelectionsHandler():
		def test_sends_command(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_character_selections', { 'status': 'pending' })
			state.network_get_character_selections_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'selections': [(p.name, p.display_name) for p in state.game.players] })

	class TestNetworkConfirmCharacterSelectionsHandler():
		def test_does_not_send_command_if_not_called_for_each_player(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_character_selections', { 'status': 'pending' })
			state.network_confirm_character_selections_handler(command_)
			command.update_and_send_to_all.assert_not_called()

		def test_sends_command_if_called_for_each_player(self, mocker, create_game):
			state = server_character_selection_state.ServerCharacterSelectionState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_character_selections', { 'status': 'pending' })
			state.network_confirm_character_selections_handler(command_)
			state.network_confirm_character_selections_handler(command_)
			command.update_and_send_to_all.assert_called_once_with(command_, { 'status': 'success' }, state.game.players)




