import pytest
import pyglet
from src.server.server_core import ServerCore, ServerGame
from src.common.grid import Player
from lattice2d.network import NetworkCommand
import types

class TestServerCore():
	class TestCreatePlayerHandler():
		def test_errors_if_name_too_short(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			command = NetworkCommand('create_player', { 'player_name': '12345' }, 'pending')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			command.update_and_send.assert_called_once_with(status='name_too_short')

		def test_errors_if_name_too_long(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			command = NetworkCommand('create_player', { 'player_name': '12345678901234567890123456' }, 'pending')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			command.update_and_send.assert_called_once_with(status='name_too_long')

		def test_errors_if_name_already_taken(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			player = Player('some name', None)
			server.players.append(player)
			command = NetworkCommand('create_player', { 'player_name': 'some name' }, 'pending')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			command.update_and_send.assert_called_once_with(status='invalid_name')

		def test_creates_player_if_successful(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			command = NetworkCommand('create_player', { 'player_name': 'some name' }, 'pending')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			assert server.players.find_by_name('some name')

		def test_sends_success_if_successful(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			command = NetworkCommand('create_player', { 'player_name': 'some name' }, 'pending')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			command.update_and_send.assert_called_once_with(status='success')

	class TestCreateGameHandler():
		def test_errors_if_name_too_short(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			command = NetworkCommand('create_game', { 'game_name': '12345' }, 'pending')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			command.update_and_send.assert_called_once_with(status='name_too_short')

		def test_errors_if_name_too_long(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			command = NetworkCommand('create_game', { 'game_name': '12345678901234567890123456789012345678901' }, 'pending')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			command.update_and_send.assert_called_once_with(status='name_too_long')

		def test_errors_if_name_already_taken(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			game = ServerGame('some name', None)
			server.children.append(game)
			command = NetworkCommand('create_game', { 'game_name': 'some name' }, 'pending')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			command.update_and_send.assert_called_once_with(status='invalid_name')

		def test_creates_game_if_successful(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			player = Player('some name', 'connection')
			server.players.append(player)
			command = NetworkCommand('create_game', { 'game_name': 'some name' }, 'pending', 'connection')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			assert server.children.find_by_name('some name')

		def test_adds_player_to_game_if_successful(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			player = Player('some name', 'connection')
			server.players.append(player)
			command = NetworkCommand('create_game', { 'game_name': 'some name' }, 'pending', 'connection')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			assert server.children.find_by_name('some name') == player.game

		def test_sends_success_if_successful(self, mocker):
			mocker.patch('lattice2d.network.Server')
			server = ServerCore()
			player = Player('some name', 'connection')
			server.players.append(player)
			command = NetworkCommand('create_game', { 'game_name': 'some name' }, 'pending', 'connection')
			mocker.patch.object(command, 'update_and_send')
			server.on_command(command)
			command.update_and_send.assert_called_once_with(status='success')
