import pytest
import pyglet
from src.server import core as core_module, game as game_module, player as player_module
from src.shared import command as command_module

@pytest.mark.usefixtures('make_core')
class TestCore():
	class TestNodeFunctionality():
		def test_allows_adding_commands_that_are_handled_on_update(self, mocker, make_core):
			core = make_core(mocker)
			command = command_module.Command('some_command_type', { 'connection': 'invalid connection' })
			core.add_command(command)
			core.on_command.assert_not_called()
			core.on_update()
			core.on_command.assert_called_once_with(command)

		def test_passes_commands_to_game_queue_if_player_has_valid_game(self, mocker, make_core):
			core = make_core(mocker, 1)
			command = command_module.Command('some_command_type', { 'connection': 'variable player connection 0' })
			core.add_command(command)
			assert core.games['variable player game'].command_queue.pop_front() == command

		def test_propogates_update_to_games(self, mocker, make_core):
			core = make_core(mocker)
			core.on_update()
			core.games['variable player game'].on_update.assert_called_once()
			core.games['fixed player game'].on_update.assert_called_once()
			core.games['empty game'].on_update.assert_called_once()

	class TestNetworkCreatePlayerHandler():
		class TestIfNameIsNotTaken():
			def test_sends_success_response(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_player', { 'player_name': 'created player', 'connection': 'created player connection' })
				core.network_create_player_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'success' })

			def test_creates_and_adds_player(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_player', { 'player_name': 'created player', 'connection': 'created player connection' })
				core.network_create_player_handler(command)
				assert core.players[-1].name == 'created player' and core.players[-1].connection == 'created player connection'

		class TestIfNameIsTaken():
			def test_sends_invalid_player_name_response(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_player', { 'player_name': 'fixed player 0', 'connection': 'fixed player connection 0' })
				core.network_create_player_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'invalid_player_name' })

	class TestNetworkCreateGameHandler():
		class TestIfNameIsNotTaken():
			def test_sends_success_response(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_game', { 'connection': 'free player connection', 'game_name': 'untaken game', 'password': 'untaken game password' })
				core.network_create_game_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'success' })

			def test_makes_player_a_host(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_game', { 'connection': 'free player connection', 'game_name': 'untaken game', 'password': 'untaken game password' })
				core.network_create_game_handler(command)
				assert core.players[-1].host

			def test_creates_a_game(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_game', { 'connection': 'free player connection', 'game_name': 'untaken game', 'password': 'untaken game password' })
				core.network_create_game_handler(command)
				assert core.games['untaken game']

			def test_sets_player_game_association(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_game', { 'connection': 'free player connection', 'game_name': 'untaken game', 'password': 'untaken game password' })
				core.network_create_game_handler(command)
				assert core.players[-1].game == core.games['untaken game']

			def test_adds_player_to_game(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_game', { 'connection': 'free player connection', 'game_name': 'untaken game', 'password': 'untaken game password' })
				core.network_create_game_handler(command)
				assert core.games['untaken game'].players == [core.players[-1]]

		class TestIfNameIsTaken():
			def test_sends_invalid_game_name_response(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_create_game', { 'connection': 'free player connection', 'game_name': 'variable player game', 'password': 'variable player game password' })
				core.network_create_game_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'invalid_game_name' })

	class TestNetworkGetGamesHandler():
		def test_sends_success_response(self, mocker, make_core):
			core = make_core(mocker, 4)
			command = command_module.Command('network_get_games', {})
			core.network_get_games_handler(command)
			command_module.update_and_send.assert_called_once_with(command, { 'status': 'success', 'games': [('variable player game', 4), ('fixed player game', 2), ('empty game', 0)] })

	class TestNetworkJoinGameHandler():
		class TestIfGameExists():
			def test_sends_success_response(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_join_game', { 'connection': 'free player connection', 'game_name': 'empty game' })
				core.network_join_game_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'success' })

			def test_sets_player_game_association(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_join_game', { 'connection': 'free player connection', 'game_name': 'empty game' })
				core.network_join_game_handler(command)
				assert core.players[-1].game == core.games['empty game']

			def test_adds_player_to_game(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_join_game', { 'connection': 'free player connection', 'game_name': 'empty game' })
				core.network_join_game_handler(command)
				assert core.games['empty game'].players == [core.players[-1]]

		class TestIfGameDoesNotExist():
			def test_sends_invalid_game_name_response(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_join_game', { 'connection': 'free player connection', 'game_name': 'nonexistent game' })
				core.network_join_game_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'invalid_game_name' })

	class TestServerDestroyGameHandler():
		def test_destroys_game(self, mocker, make_core):
			core = make_core(mocker)
			command = command_module.Command('server_destroy_game', { 'game_name': 'variable player game' })
			core.server_destroy_game_handler(command)
			assert 'variable player game' not in core.games.keys()

	class TestNetworkLogoutHandler():
		class TestWhenPlayerIsInAGame():
			def test_sends_success_response(self, mocker, make_core):
				core = make_core(mocker, 2)
				command = command_module.Command('network_logout', { 'connection': 'variable player connection 0' })
				core.network_logout_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'success' })

			def test_removes_player_from_game(self, mocker, make_core):
				core = make_core(mocker, 2)
				command = command_module.Command('network_logout', { 'connection': 'variable player connection 0' })
				core.network_logout_handler(command)
				assert len(core.games['variable player game'].players) == 1

			def test_destroys_game_if_last_person_in_game_leaves(self, mocker, make_core):
				core = make_core(mocker, 1)
				command = command_module.Command('network_logout', { 'connection': 'variable player connection 0' })
				core.network_logout_handler(command)
				assert 'variable player game' not in core.games.keys()

			def test_broadcasts_players_in_game_if_still_players_in_game(self, mocker, make_core):
				core = make_core(mocker, 2)
				command = command_module.Command('network_logout', { 'connection': 'variable player connection 0' })
				core.network_logout_handler(command)
				assert core.games['variable player game'].command_queue.pop_front().type == 'server_broadcast_players'

			def test_destroys_player(self, mocker, make_core):
				core = make_core(mocker, 2)
				command = command_module.Command('network_logout', { 'connection': 'variable player connection 0' })
				core.network_logout_handler(command)
				assert 'variable player connection 0' not in core.players

		class TestWhenPlayerIsNotInAGame():
			def test_destroys_player(self, mocker, make_core):
				core = make_core(mocker)
				command = command_module.Command('network_logout', { 'connection': 'free player connection' })
				core.network_logout_handler(command)
				assert 'free player connection' not in core.players
