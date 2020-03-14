import pytest
import pyglet
from src.server.states import lobby_state as lobby_state_module, character_selection_state as character_selection_state_module
from src.shared import command as command_module

@pytest.mark.usefixtures('make_lobby_state')
class TestLobbyState():
	class TestNetworkGetPlayersInGameHandler():
		class TestIfGivenException():
			def test_sends_success_response_to_all_except_exception(self, mocker, make_lobby_state):
				lobby_state = make_lobby_state(mocker, 3)
				command = command_module.Command('network_get_players_in_game', { 'exception': 'player connection 0' })
				lobby_state.network_get_players_in_game_handler(command)
				assert command_module.create_and_send.call_count == 2
				assert command_module.create_and_send.call_args_list[0] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 1' 
					}
				)
				assert command_module.create_and_send.call_args_list[1] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 2' 
					}
				)

		class TestIfNotGivenException():
			def test_sends_success_response_to_all_players(self, mocker, make_lobby_state):
				lobby_state = make_lobby_state(mocker, 3)
				command = command_module.Command('network_get_players_in_game', { 'exception': None })
				lobby_state.network_get_players_in_game_handler(command)
				assert command_module.create_and_send.call_count == 3
				assert command_module.create_and_send.call_args_list[0] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 0' 
					}
				)
				assert command_module.create_and_send.call_args_list[1] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 1' 
					}
				)
				assert command_module.create_and_send.call_args_list[2] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 2' 
					}
				)

	class TestServerBroadcastPlayersHandler():
		class TestIfGivenException():
			def test_sends_success_response_to_all_except_exception(self, mocker, make_lobby_state):
				lobby_state = make_lobby_state(mocker, 3)
				command = command_module.Command('server_broadcast_players', { 'exception': 'player connection 0' })
				lobby_state.server_broadcast_players_handler(command)
				assert command_module.create_and_send.call_count == 2
				assert command_module.create_and_send.call_args_list[0] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 1' 
					}
				)
				assert command_module.create_and_send.call_args_list[1] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 2' 
					}
				)

		class TestIfNotGivenException():
			def test_sends_success_response_to_all_players(self, mocker, make_lobby_state):
				lobby_state = make_lobby_state(mocker, 3)
				command = command_module.Command('server_broadcast_players', { 'exception': None })
				lobby_state.server_broadcast_players_handler(command)
				assert command_module.create_and_send.call_count == 3
				assert command_module.create_and_send.call_args_list[0] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 0' 
					}
				)
				assert command_module.create_and_send.call_args_list[1] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 1' 
					}
				)
				assert command_module.create_and_send.call_args_list[2] == mocker.call(
					'network_get_players_in_game',
					{ 
						'status': 'success', 
						'game_name': 'game name', 
						'players': [('player 0', True), ('player 1', False), ('player 2', False)],
						'connection': 'player connection 2' 
					}
				)

	class TestNetworkStartGameHandler():
		class TestIfSentByHost():
			def test_sets_state(self, mocker, make_lobby_state):
				lobby_state = make_lobby_state(mocker, 3)
				command = command_module.Command('network_start_game', { 'connection': 'player connection 0' })
				lobby_state.network_start_game_handler(command)
				assert lobby_state.set_state.call_count == 1
				assert isinstance(lobby_state.set_state.call_args_list[0][0][0], character_selection_state_module.CharacterSelectionState) 

			def test_sends_success_response_to_players(self, mocker, make_lobby_state):
				lobby_state = make_lobby_state(mocker, 3)
				command = command_module.Command('network_start_game', { 'connection': 'player connection 0' })
				lobby_state.network_start_game_handler(command)
				assert command_module.update_and_send.call_count == 3
				command_module.update_and_send.assert_has_calls([
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 0' }),
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 1' }),
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 2' })
				], any_order=True)

		class TestIfNotSentByHost():
			def test_sends_not_host_response(self, mocker, make_lobby_state):
				lobby_state = make_lobby_state(mocker, 3)
				command = command_module.Command('network_start_game', { 'connection': 'player connection 1' })
				lobby_state.network_start_game_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'not_host' })
