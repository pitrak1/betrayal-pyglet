import pytest
import pyglet
from src.server.states import lobby_state, server_character_selection_state
from src.common import command
import types
import random

class TestLobbyState():
	class TestNetworkStartGameHandler():
		def test_sends_error_command_with_less_than_2_players(self, mocker, create_game):
			state = lobby_state.LobbyState(create_game(mocker, player_count=1))
			command_ = command.Command('network_start_game', { 'status': 'pending' })
			state.network_start_game_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'not_enough_players' })

		def test_sets_state_to_character_selection_state_with_more_than_1_player(self, mocker, get_args, create_game):
			state = lobby_state.LobbyState(create_game(mocker, player_count=2))
			command_ = command.Command('network_start_game', { 'status': 'pending' })
			state.network_start_game_handler(command_)
			assert isinstance(get_args(state.game.set_state, 0, 0), server_character_selection_state.ServerCharacterSelectionState)

		def test_sends_success_command_to_all_with_more_than_1_player(self, mocker, create_game):
			state = lobby_state.LobbyState(create_game(mocker, player_count=2))
			command_ = command.Command('network_start_game', { 'status': 'pending' })
			state.network_start_game_handler(command_)
			command.update_and_send_to_all.assert_called_once_with(command_, { 'status': 'success' }, state.game.players)
