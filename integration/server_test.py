import pytest
from src.server.states import LobbyState, SetupState
from integration import helpers
from lattice2d.command import Command

class TestLobbyState():
	def test_starts_in_lobby_state(self, mocker):
		game = helpers.create_game(mocker)
		assert helpers.is_state(game, LobbyState)

	class TestStartGame():
		def test_responds_with_error_if_not_enough_players(self, mocker, get_keyword_args):
			game = helpers.create_game(mocker, 0)
			command = Command('start_game', {}, 'pending')
			helpers.add_stubbed_command(mocker, game, command)
			assert get_keyword_args(command.update_and_send, 0, 'status') == 'not_enough_players'

		def test_transitions_if_enough_players(self, mocker):
			game = helpers.create_game(mocker, 2)
			command = Command('start_game', {}, 'pending')
			helpers.add_stubbed_command(mocker, game, command)
			assert helpers.is_state(game, SetupState)

		def test_responds_with_success_to_each_player_if_enough_players(self, mocker, get_keyword_args):
			game = helpers.create_game(mocker, 2)
			command = Command('start_game', {}, 'pending')
			helpers.add_stubbed_command(mocker, game, command)
			assert command.update_and_send.call_count == 2
			assert get_keyword_args(command.update_and_send, 0, 'status') == 'success'
			assert get_keyword_args(command.update_and_send, 1, 'status') == 'success'


