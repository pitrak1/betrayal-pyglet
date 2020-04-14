import pytest
import pyglet
from src.server import game
from src.common import command
import types

class TestGame():
	class TestAddPlayer():
		def test_sets_player_game(self, mocker, create_player):
			game_ = game.Game('game0')
			player = create_player(mocker, 'player0')
			game_.add_player(player)
			assert player.game == game_

		def test_adds_player_to_game(self, mocker, create_player):
			game_ = game.Game('game0')
			player = create_player(mocker, 'player0')
			game_.add_player(player)
			assert game_.players == [player]

	class TestRemovePlayer():
		def test_sets_player_game_to_none(self, mocker, create_player):
			game_ = game.Game('game0')
			player = create_player(mocker, 'player0')
			game_.add_player(player)
			game_.remove_player(player)
			assert player.game == None

		def test_removes_player_from_game(self, mocker, create_player):
			game_ = game.Game('game0')
			player = create_player(mocker, 'player0')
			game_.add_player(player)
			game_.remove_player(player)
			assert game_.players == []

		def test_sends_players_in_game_if_players_remaining(self, mocker, create_player):
			game_ = game.Game('game0')
			player0 = create_player(mocker, 'player0')
			player1 = create_player(mocker, 'player1')
			game_.add_player(player0)
			game_.add_player(player1)
			game_.remove_player(player0)
			command.create_and_send_to_all.assert_called_once_with(
				'network_get_players_in_game', 
				{ 'status': 'success', 'players': [('player1', False)] }, 
				game_.players
			)

		def test_sends_destroy_if_no_players_remaining(self, mocker, create_player):
			game_ = game.Game('game0')
			player0 = create_player(mocker, 'player0')
			game_.add_player(player0)
			game_.remove_player(player0)
			assert game_.command_queue.pop_front().type == 'server_destroy_game'

	class TestSendPlayersInGame():
		def test_sends_players_in_game(self, mocker, create_player):
			game_ = game.Game('game0')
			player0 = create_player(mocker, 'player0')
			player1 = create_player(mocker, 'player1')
			game_.add_player(player0)
			game_.add_player(player1)
			game_.send_players_in_game()
			command.create_and_send_to_all.assert_called_once_with(
				'network_get_players_in_game', 
				{ 'status': 'success', 'players': [('player0', False), ('player1', False)] }, 
				game_.players
			)

		def test_sends_players_in_game_to_all_but_exception_if_exception_given(self, mocker, create_player):
			game_ = game.Game('game0')
			player0 = create_player(mocker, 'player0')
			player1 = create_player(mocker, 'player1')
			game_.add_player(player0)
			game_.add_player(player1)
			game_.send_players_in_game(player0)
			command.create_and_send_to_all.assert_called_once_with(
				'network_get_players_in_game', 
				{ 'status': 'success', 'players': [('player0', False), ('player1', False)] }, 
				[player1]
			)
