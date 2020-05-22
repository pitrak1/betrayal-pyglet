import pytest
import pyglet
from src.server.server_states import ServerLobbyState, ServerSetupState, ServerGameState
from src.server.server_grid import ServerPlayer
from lattice2d.network import NetworkCommand
from lattice2d.full.full_server import FullServerGame

class TestServerStates():
	class TestServerLobbyState():
		class TestNetworkStartGameHandler():
			def test_errors_if_not_enough_players(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				state = ServerLobbyState(game)
				command = NetworkCommand('network_start_game', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				command.update_and_send.assert_called_once_with(status='not_enough_players')

			def test_sets_state_to_setup_if_success(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player = ServerPlayer('player 1', 'connection 1')
				game.players.append(player)
				state = ServerLobbyState(game)
				command = NetworkCommand('network_start_game', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				assert isinstance(game.current_state, ServerSetupState)

			def test_responds_to_each_player_if_success(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerLobbyState(game)
				command = NetworkCommand('network_start_game', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				assert command.update_and_send.call_count == 2

	class TestServerSetupState():
		class TestNetworkGetPlayerOrderHandler():
			def test_returns_players_in_order(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_get_player_order', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				command.update_and_send.assert_called_once_with(status='success', data={ 'players': ['player 1', 'player 2'] })

		class TestNetworkConfirmPlayerOrderHandler():
			def test_does_not_respond_if_not_called_for_each_player(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_confirm_player_order', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				command.update_and_send.assert_not_called()

			def test_responds_if_called_for_each_player(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_confirm_player_order', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				state.on_command(command)
				assert command.update_and_send.call_count == 2

		class TestNetworkGetAvailableCharactersHandler():
			def test_returns_characters(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				state = ServerSetupState(game)
				command = NetworkCommand('network_get_available_characters', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				command.update_and_send.assert_called_once_with(status='success', data={ 'characters': state.characters })

		class TestNetworkSelectCharacterHandler():
			def test_sets_character_for_player(self, mocker):
				mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_select_character', { 'character': 'heather_granville' }, 'pending', player2.connection)
				state.on_command(command)
				assert player2.variable_name == 'heather_granville'

			def test_removes_character(self, mocker):
				mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_select_character', { 'character': 'heather_granville' }, 'pending', player2.connection)
				state.on_command(command)
				assert 'heather_granville' not in state.characters

			def test_moves_to_next_player(self, mocker):
				mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_select_character', { 'character': 'heather_granville' }, 'pending', player2.connection)
				state.on_command(command)
				assert game.get_current_player() == player1

			def test_broadcasts_updated_characters_if_all_players_have_not_selected(self, mocker, get_args):
				mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_select_character', { 'character': 'heather_granville' }, 'pending', player2.connection)
				state.on_command(command)
				assert NetworkCommand.create_and_send.call_count == 2
				assert get_args(NetworkCommand.create_and_send, 0, 0) == 'network_get_available_characters'

			def test_broadcasts_all_selected_if_all_players_have_selected(self, mocker, get_args):
				mocker.patch('lattice2d.network.NetworkCommand.create_and_send')
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				state = ServerSetupState(game)
				command = NetworkCommand('network_select_character', { 'character': 'heather_granville' }, 'pending', player1.connection)
				state.on_command(command)
				assert NetworkCommand.create_and_send.call_count == 1
				assert get_args(NetworkCommand.create_and_send, 0, 0) == 'network_all_characters_selected'

		class TestNetworkGetCharacterSelectionsHandler():
			def test_gets_selected_character_for_each_player(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				player1.display_name = 'Player 1 Character'
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				player2.display_name = 'Player 2 Character'
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_get_character_selections', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				command.update_and_send.assert_called_once_with(status='success', data={ 
					'selections': [('player 1', 'Player 1 Character'), ('player 2', 'Player 2 Character')] 
				})

		class TestNetworkConfirmPlayerSelectionsHandler():
			def test_does_not_respond_if_not_called_for_each_player(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_confirm_character_selections', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				command.update_and_send.assert_not_called()

			def test_responds_if_called_for_each_player(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_confirm_character_selections', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				state.on_command(command)
				assert command.update_and_send.call_count == 2

			def test_sets_state_to_game_if_called_for_each_player(self, mocker):
				game = FullServerGame('game name', mocker.stub())
				player1 = ServerPlayer('player 1', 'connection 1')
				game.players.append(player1)
				player2 = ServerPlayer('player 2', 'connection 2')
				game.players.append(player2)
				state = ServerSetupState(game)
				command = NetworkCommand('network_confirm_character_selections', {}, 'pending')
				mocker.patch.object(command, 'update_and_send')
				state.on_command(command)
				state.on_command(command)
				assert isinstance(game.current_state, ServerGameState)
