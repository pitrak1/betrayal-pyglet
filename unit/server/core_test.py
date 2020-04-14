import pytest
import pyglet
from src.server import core, server_player
from src.common import command, constants
import types

class TestCore():
	class TestServerDestroyGameHandler():
		def test_destroys_game(self, mocker):
			core_ = core.Core()
			core_.games['game0'] = 'game0'
			command_ = command.Command('server_destroy_game', { 'game_name': 'game0' })
			core_.server_destroy_game_handler(command_)
			assert 'game0' not in core_.games.keys()

	class TestNetworkCreatePlayerHandler():
		def test_sends_error_if_name_too_short(self, mocker):
			core_ = core.Core()
			command_ = command.Command('network_create_player', { 'player_name': 'playe', 'connection': 'player0_connection' })
			core_.network_create_player_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'name_too_short' })

		def test_sends_error_if_name_too_long(self, mocker):
			core_ = core.Core()
			command_ = command.Command('network_create_player', { 'player_name': 'player01234567890123456789', 'connection': 'player0_connection' })
			core_.network_create_player_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'name_too_long' })

		def test_sends_error_if_name_already_exists(self, mocker, create_player):
			core_ = core.Core()
			player = create_player(mocker, 'player0')
			core_.players.append(player)
			command_ = command.Command('network_create_player', { 'player_name': 'player0', 'connection': 'player0_connection' })
			core_.network_create_player_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'invalid_player_name' })

		def test_adds_player_if_valid(self, mocker):
			core_ = core.Core()
			command_ = command.Command('network_create_player', { 'player_name': 'player0', 'connection': 'player0_connection' })
			core_.network_create_player_handler(command_)
			assert isinstance(core_.players[0], server_player.ServerPlayer)
			assert core_.players[0].name == 'player0'

		def test_sends_success_if_valid(self, mocker, create_player):
			core_ = core.Core()
			command_ = command.Command('network_create_player', { 'player_name': 'player0', 'connection': 'player0_connection' })
			core_.network_create_player_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success' })

	class TestNetworkGetGamesHandler():
		def test_sends_games(self, mocker, create_game):
			core_ = core.Core()
			core_.games['game0'] = create_game(mocker, 'game0', 2)
			core_.games['game1'] = create_game(mocker, 'game1', 3)
			command_ = command.Command('network_get_games', {})
			core_.network_get_games_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success', 'games': [('game0', 2), ('game1', 3)] })

	class TestNetworkJoinGameHandler():
		def test_sends_error_if_game_full(self, mocker, create_game):
			core_ = core.Core()
			core_.games['game0'] = create_game(mocker, 'game0', constants.PLAYERS_PER_GAME)
			command_ = command.Command('network_join_game', { 'game_name': 'game0' })
			core_.network_join_game_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'game_full' })

		def test_sets_player_game(self, mocker, create_game, create_player):
			core_ = core.Core()
			game = create_game(mocker, 'game0')
			core_.games['game0'] = game
			player = create_player(mocker, 'player0')
			core_.players.append(player)
			command_ = command.Command('network_join_game', { 'game_name': 'game0', 'connection': 'player0_connection' })
			core_.network_join_game_handler(command_)
			assert player.game == game

		def test_adds_player_to_game(self, mocker, create_game, create_player):
			core_ = core.Core()
			game = create_game(mocker, 'game0')
			core_.games['game0'] = game
			player = create_player(mocker, 'player0')
			core_.players.append(player)
			command_ = command.Command('network_join_game', { 'game_name': 'game0', 'connection': 'player0_connection' })
			core_.network_join_game_handler(command_)
			assert game.players == [player]

		def test_adds_command_to_broadcast_players(self, mocker, get_args, create_game, create_player):
			core_ = core.Core()
			game = create_game(mocker, 'game0')
			core_.games['game0'] = game
			player = create_player(mocker, 'player0')
			core_.players.append(player)
			mocker.patch.object(core_, 'add_command')
			command_ = command.Command('network_join_game', { 'game_name': 'game0', 'connection': 'player0_connection' })
			core_.network_join_game_handler(command_)
			assert get_args(core_.add_command, 0, 0).type == 'server_broadcast_players'

		def test_sends_success(self, mocker, get_args, create_game, create_player):
			core_ = core.Core()
			game = create_game(mocker, 'game0')
			core_.games['game0'] = game
			player = create_player(mocker, 'player0')
			core_.players.append(player)
			command_ = command.Command('network_join_game', { 'game_name': 'game0', 'connection': 'player0_connection' })
			core_.network_join_game_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success' })

	class TestNetworkLogoutHandler():
		def test_removes_player_from_game_if_player_in_game(self, mocker, create_game):
			core_ = core.Core()
			game = create_game(mocker, 'game0', 1)
			core_.games['game0'] = game
			player = game.players[0]
			core_.players.append(player)
			command_ = command.Command('network_logout', { 'connection': 'player0_connection' })
			core_.network_logout_handler(command_)
			game.remove_player.assert_called_once_with(player)

		def test_removes_player_from_players(self, mocker, create_player):
			core_ = core.Core()
			player = create_player(mocker, 'player0')
			core_.players.append(player)
			command_ = command.Command('network_logout', { 'connection': 'player0_connection' })
			core_.network_logout_handler(command_)
			assert core_.players == []

		def test_sends_success(self, mocker, create_player):
			core_ = core.Core()
			player = create_player(mocker, 'player0')
			core_.players.append(player)
			command_ = command.Command('network_logout', { 'connection': 'player0_connection' })
			core_.network_logout_handler(command_)
			command.update_and_send.assert_called_once_with(command_, { 'status': 'success' })

	class TestAddCommand():
		def test_adds_to_game_queue_if_player_in_game(self, mocker, create_game):
			core_ = core.Core()
			game = create_game(mocker, 'game0', 1)
			core_.games['game0'] = game
			player = game.players[0]
			core_.players.append(player)
			command_ = command.Command('some_generic_command_type', { 'connection': 'player0_connection' })
			core_.add_command(command_)
			assert game.command_queue[0] == command_

		def test_adds_to_core_queue_if_player_not_in_game(self, mocker, create_player):
			core_ = core.Core()
			player = create_player(mocker, 'player0')
			core_.players.append(player)
			command_ = command.Command('some_generic_command_type', { 'connection': 'player0_connection' })
			core_.add_command(command_)
			assert core_.command_queue.pop_front() == command_


