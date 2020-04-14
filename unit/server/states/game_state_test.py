import pytest
import pyglet
from src.server.states import game_state
from src.common import command
import types
import random

class TestGameState():
	class TestNetworkGetPlayerPositionsHandler():
		def test_sends_players_with_positions(self, mocker, create_game):
			state = game_state.GameState(create_game(mocker, player_count=1))
			command_ = command.Command('network_get_player_positions', {})
			state.network_get_player_positions_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'players': [('player0', 'player0_variable_name', 0, 0)] })

	class TestNetworkGetCurrentPlayerHandler():
		def test_sends_self_if_current_player(self, mocker, create_game):
			state = game_state.GameState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_current_player', { 'connection': 'player0_connection' })
			state.network_get_current_player_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'player_name': 'self' })

		def test_sends_player_name_if_not_current_player(self, mocker, create_game):
			state = game_state.GameState(create_game(mocker, player_count=2))
			command_ = command.Command('network_get_current_player', { 'connection': 'player1_connection' })
			state.network_get_current_player_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'player_name': 'player0' })
