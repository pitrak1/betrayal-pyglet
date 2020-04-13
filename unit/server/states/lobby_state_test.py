import pytest
import pyglet
from src.server.states import lobby_state, server_character_selection_state
from src.common import command
import types
import random

class TestLobbyState():
	def create_game(self, mocker, players=[]):
		game = types.SimpleNamespace()
		game.name = 'game name'
		game.players = players
		game.set_state = mocker.stub()
		return game

	def test_sends_error_command_on_start_game_with_less_than_2_players(self, mocker):
		random.seed(0)
		state = lobby_state.LobbyState(self.create_game(mocker, ['player1']))
		command_ = command.Command('network_start_game', { 'status': 'pending' })
		mocker.patch('src.common.command.update_and_send')
		state.network_start_game_handler(command_)
		command.update_and_send.assert_called_once_with(command_, { 'status': 'not_enough_players' })

	def test_sets_state_to_character_selection_state_on_start_game_with_more_than_1_player(self, mocker, get_args):
		random.seed(0)
		state = lobby_state.LobbyState(self.create_game(mocker, ['player1', 'player2']))
		command_ = command.Command('network_start_game', { 'status': 'pending' })
		mocker.patch('src.common.command.update_and_send_to_all')
		state.network_start_game_handler(command_)
		assert isinstance(get_args(state.game.set_state, 0, 0), server_character_selection_state.ServerCharacterSelectionState)

	def test_sends_success_command_to_all_on_start_game_with_more_than_1_player(self, mocker):
		random.seed(0)
		state = lobby_state.LobbyState(self.create_game(mocker, ['player1', 'player2']))
		command_ = command.Command('network_start_game', { 'status': 'pending' })
		mocker.patch('src.common.command.update_and_send_to_all')
		state.network_start_game_handler(command_)
		command.update_and_send_to_all.assert_called_once_with(command_, { 'status': 'success' }, ['player1', 'player2'])
