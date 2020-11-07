import pytest
import pyglet
from integration import helpers
from lattice2d.config import Config
from src.server.server_core import ServerCore
from src.client.menu_states import SplashState, CreatePlayerState, MainMenuState, CreateGameState, GameListState, LobbyState
from src.client.setup_states import PlayerOrderState
from lattice2d.command import Command
from config import CONFIG
import sys

class TestMenu():
	class TestSplashState():
		def test_starts_in_splash_state(self):
			client = helpers.create_client()
			assert helpers.is_state(client, SplashState)

		def test_transitions_to_create_player_state(self):
			client = helpers.create_client()
			helpers.click_button(client, 'begin_button')
			assert helpers.is_state(client, CreatePlayerState)

	class TestCreatePlayerState():
		class TestExitButton():
			def test_exits_when_clicked(self, mocker):
				client = helpers.create_client()
				mocker.patch('sys.exit')
				helpers.to_menu_create_player_state(client)
				helpers.click_button(client, 'exit_button')
				sys.exit.assert_called_once()

		class TestNameInput():
			def test_does_not_send_command_if_player_name_is_too_short(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_create_player_state(client)
				helpers.enter_text(client, 'name_input', '12345')
				helpers.click_button(client, 'continue_button')
				assert not client.command_queue.has_elements()

			def test_truncates_player_name_if_player_name_is_too_long(self):
				client = helpers.create_client()
				helpers.to_menu_create_player_state(client)
				helpers.enter_text(client, 'name_input', '123456789012345678901234567890')
				assert len(helpers.get_text(client, 'name_input')) == 23

			def test_sends_command_if_player_name_is_appropriate_length(self, mocker, get_positional_args):
				client = helpers.create_client()
				helpers.to_menu_create_player_state(client)
				helpers.enter_text(client, 'name_input', '1234567890')
				mocker.patch.object(client.current_state, 'add_command')
				helpers.click_button(client, 'continue_button')
				command = get_positional_args(client.current_state.add_command, 0, 0)
				assert command.type == 'create_player'

		class TestNameInputResponse():
			def test_does_not_transition_if_status_is_not_success(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_create_player_state(client)
				helpers.add_command(client, Command('create_player', { 'player_name': 'player1' }, 'invalid_name'))
				assert helpers.is_state(client, CreatePlayerState)

			def test_transitions_if_status_is_success(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_create_player_state(client)
				helpers.add_command(client, Command('create_player', { 'player_name': 'player1' }, 'success'))
				assert helpers.is_state(client, MainMenuState)

	class TestMainMenuState():
		def test_sends_command_if_exit_is_clicked(self, mocker, get_positional_args):
			client = helpers.create_client()
			helpers.to_menu_main_menu_state(client)
			mocker.patch.object(client.current_state, 'add_command')
			helpers.click_button(client, 'exit_button')
			command = get_positional_args(client.current_state.add_command, 0, 0)
			assert command.type == 'logout'

		def test_exits_if_logout_is_successful(self, mocker):
			client = helpers.create_client()
			mocker.patch('sys.exit')
			helpers.to_menu_main_menu_state(client)
			helpers.add_command(client, Command('logout', {}, 'success'))
			sys.exit.assert_called()

		def test_does_not_exit_if_logout_is_unsuccessful(self, mocker):
			client = helpers.create_client()
			mocker.patch('sys.exit')
			helpers.to_menu_main_menu_state(client)
			helpers.add_command(client, Command('logout', {}, 'unsuccess'))
			sys.exit.assert_not_called()

		def test_transitions_if_create_game_button_is_clicked(self, mocker):
			client = helpers.create_client()
			helpers.to_menu_main_menu_state(client)
			helpers.click_button(client, 'create_button')
			assert helpers.is_state(client, CreateGameState)

		def test_transitions_if_join_game_button_is_clicked(self, mocker):
			client = helpers.create_client()
			helpers.to_menu_main_menu_state(client)
			helpers.click_button(client, 'join_button')
			assert helpers.is_state(client, GameListState)

	class TestCreateGameState():
		class TestNameInput():
			def test_does_not_send_command_if_game_name_is_too_short(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_create_game_state(client)
				helpers.enter_text(client, 'name_input', '12345')
				helpers.click_button(client, 'create_button')
				assert not client.command_queue.has_elements()

			def test_truncates_player_name_if_player_name_is_too_long(self):
				client = helpers.create_client()
				helpers.to_menu_create_game_state(client)
				helpers.enter_text(client, 'name_input', '12345678901234567890123456789012345678901234567890')
				assert len(helpers.get_text(client, 'name_input')) == 40

			def test_sends_command_if_game_name_is_appropriate_length(self, mocker, get_positional_args):
				client = helpers.create_client()
				helpers.to_menu_create_game_state(client)
				helpers.enter_text(client, 'name_input', '1234567890')
				mocker.patch.object(client.current_state, 'add_command')
				helpers.click_button(client, 'create_button')
				command = get_positional_args(client.current_state.add_command, 0, 0)
				assert command.type == 'create_game'

		class TestNameInputResponse():
			def test_does_not_transition_if_status_is_not_success(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_create_game_state(client)
				helpers.add_command(client, Command('create_game', { 'game_name': 'lobby1' }, 'invalid_name'))
				assert helpers.is_state(client, CreateGameState)

			def test_transitions_if_status_is_success(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_create_game_state(client)
				helpers.add_command(client, Command('create_game', { 'game_name': 'lobby1' }, 'success'))
				assert helpers.is_state(client, LobbyState)

	class TestGameListState():
		def test_transitions_if_back_button_is_clicked(self, mocker):
			client = helpers.create_client()
			helpers.to_menu_game_list_state(client)
			helpers.click_button(client, 'back_button')
			assert helpers.is_state(client, MainMenuState)

		class TestGetGamesResponse():
			def test_draws_games_if_command_is_successful(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3]
				]}, 'success'))
				assert client.current_state.get_component('game_0')
				assert client.current_state.get_component('game_1')
				with pytest.raises(AssertionError):
					client.current_state.get_component('game_2')

			def test_does_not_draw_arrows_if_less_than_1_page(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3]
				]}, 'success'))
				with pytest.raises(AssertionError):
					client.current_state.get_component('down_button')
				with pytest.raises(AssertionError):
					client.current_state.get_component('up_button')

			def test_does_not_draw_arrows_if_exactly_1_page(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3],
					['lobby3', 4],
					['lobby4', 1]
				]}, 'success'))
				with pytest.raises(AssertionError):
					client.current_state.get_component('down_button')
				with pytest.raises(AssertionError):
					client.current_state.get_component('up_button')

			def test_only_draws_down_arrow_if_more_than_1_page(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3],
					['lobby3', 4],
					['lobby4', 1],
					['lobby5', 3]
				]}, 'success'))
				assert client.current_state.get_component('down_button')
				with pytest.raises(AssertionError):
					client.current_state.get_component('up_button')

			def test_draws_second_page(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3],
					['lobby3', 4],
					['lobby4', 1],
					['lobby5', 3],
					['lobby6', 2],
					['lobby7', 4]
				]}, 'success'))
				helpers.click_button(client, 'down_button')
				assert client.current_state.get_component('game_0')
				assert client.current_state.get_component('game_1')
				assert client.current_state.get_component('game_2')
				with pytest.raises(AssertionError):
					client.current_state.get_component('game_3')

			def test_does_not_draw_down_arrow_if_count_less_than_page(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3],
					['lobby3', 4],
					['lobby4', 1],
					['lobby5', 3],
					['lobby6', 2],
					['lobby7', 4]
				]}, 'success'))
				helpers.click_button(client, 'down_button')
				with pytest.raises(AssertionError):
					client.current_state.get_component('down_button')

			def test_does_not_draw_down_arrow_if_count_is_exactly_page(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3],
					['lobby3', 4],
					['lobby4', 1],
					['lobby5', 3],
					['lobby6', 2],
					['lobby7', 4],
					['lobby8', 3]
				]}, 'success'))
				helpers.click_button(client, 'down_button')
				with pytest.raises(AssertionError):
					client.current_state.get_component('down_button')

			def test_draws_up_arrow_if_not_on_first_page(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3],
					['lobby3', 4],
					['lobby4', 1],
					['lobby5', 3],
					['lobby6', 2],
					['lobby7', 4],
					['lobby8', 3]
				]}, 'success'))
				helpers.click_button(client, 'down_button')
				assert client.current_state.get_component('up_button')

			def test_allows_going_back_pages(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 4],
					['lobby2', 3],
					['lobby3', 4],
					['lobby4', 1],
					['lobby5', 3],
					['lobby6', 2]
				]}, 'success'))
				helpers.click_button(client, 'down_button')
				helpers.click_button(client, 'up_button')
				assert client.current_state.get_component('game_0')
				assert client.current_state.get_component('game_1')
				assert client.current_state.get_component('game_2')
				assert client.current_state.get_component('game_3')

		def test_sends_command_if_refresh_is_clicked(self, mocker, get_positional_args):
			client = helpers.create_client()
			helpers.to_menu_game_list_state(client)
			helpers.add_command(client, Command('get_games', { 'games': [
				['lobby1', 4],
				['lobby2', 3],
				['lobby3', 4],
				['lobby4', 1],
				['lobby5', 3],
				['lobby6', 2]
			]}, 'success'))
			mocker.patch.object(client.current_state, 'add_command')
			helpers.click_button(client, 'refresh')
			command = get_positional_args(client.current_state.add_command, 0, 0)
			assert command.type == 'get_games'

		class TestJoin():
			def test_does_not_send_command_if_game_is_full(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 6],
					['lobby2', 3]
				]}, 'success'))
				helpers.click_button(client, 'game_0')
				assert not client.command_queue.has_elements()

			def test_sends_command_if_game_is_not_full(self, mocker, get_positional_args):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('get_games', { 'games': [
					['lobby1', 6],
					['lobby2', 3]
				]}, 'success'))
				mocker.patch.object(client.current_state, 'add_command')
				helpers.click_button(client, 'game_1')
				command = get_positional_args(client.current_state.add_command, 0, 0)
				assert command.type == 'join_game'

		class TestJoinResponse():
			def test_does_not_transition_if_status_is_not_success(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('join_game', { 'game_name': 'lobby1' }, 'game_full'))
				assert helpers.is_state(client, GameListState)

			def test_transitions_if_status_is_success(self, mocker):
				client = helpers.create_client()
				helpers.to_menu_game_list_state(client)
				helpers.add_command(client, Command('join_game', { 'game_name': 'lobby2' }, 'success'))
				assert helpers.is_state(client, LobbyState)

	class TestLobbyState():
		class TestBroadcastPlayersInGameResponse():
			def test_draws_players_if_command_is_successful(self, mocker):
				client = helpers.create_client()
				helpers.to_lobby_state_as_host(client)
				helpers.add_command(client, Command('broadcast_players_in_game', { 'players': [
					['player1', False],
					['player2', True]
				]}, 'success'))
				assert client.current_state.get_component('player_0')
				assert client.current_state.get_component('player_1')
				with pytest.raises(AssertionError):
					client.current_state.get_component('player_2')

		class TestLeaveGame():
			def test_sends_command_if_back_button_is_clicked(self, mocker, get_positional_args):
				client = helpers.create_client()
				helpers.to_lobby_state_as_host(client)
				mocker.patch.object(client.current_state, 'add_command')
				helpers.click_button(client, 'back_button')
				command = get_positional_args(client.current_state.add_command, 0, 0)
				assert command.type == 'leave_game'

		class TestLeaveGameResponse():
			def test_does_not_transition_if_status_is_not_success(self, mocker):
				client = helpers.create_client()
				helpers.to_lobby_state_as_host(client)
				helpers.add_command(client, Command('leave_game', {}, 'unsuccessful'))
				assert helpers.is_state(client, LobbyState)

			def test_transitions_if_status_is_success(self, mocker):
				client = helpers.create_client()
				helpers.to_lobby_state_as_host(client)
				helpers.add_command(client, Command('leave_game', {}, 'success'))
				assert helpers.is_state(client, MainMenuState)

		def test_does_not_draw_start_button_if_not_host(self, mocker):
			client = helpers.create_client()
			helpers.to_lobby_state_as_player(client)
			with pytest.raises(AssertionError):
				client.current_state.get_component('start_button')

		def test_draws_start_button_if_host(self, mocker):
			client = helpers.create_client()
			helpers.to_lobby_state_as_host(client)
			assert client.current_state.get_component('start_button')

		class TestStartGame():
			def test_does_not_send_command_if_not_enough_players(self, mocker):
				client = helpers.create_client()
				helpers.to_lobby_state_as_host(client)
				helpers.add_command(client, Command('broadcast_players_in_game', { 'players': [] }, 'success'))
				helpers.click_button(client, 'start_button')
				assert not client.command_queue.has_elements()

			def test_sends_command_if_enough_players(self, mocker, get_positional_args):
				client = helpers.create_client()
				helpers.to_lobby_state_as_host(client)
				helpers.add_command(client, Command('broadcast_players_in_game', { 'players': [
					['player1', True],
					['player2', False]
				] }, 'success'))
				mocker.patch.object(client.current_state, 'add_command')
				helpers.click_button(client, 'start_button')
				command = get_positional_args(client.current_state.add_command, 0, 0)
				assert command.type == 'start_game'

		class TestStartGameResponse():
			def test_does_not_transition_if_not_successful(self, mocker):
				client = helpers.create_client()
				helpers.to_lobby_state_as_host(client)
				helpers.add_command(client, Command('start_game', {}, 'not_enough_players'))
				assert helpers.is_state(client, LobbyState)

			def test_transitions_if_status_is_success(self, mocker):
				client = helpers.create_client()
				helpers.to_lobby_state_as_host(client)
				helpers.add_command(client, Command('start_game', {}, 'success'))
				assert helpers.is_state(client, PlayerOrderState)