import pytest
import pyglet
from integration import helpers
from lattice2d.states import StateMachine
from lattice2d.config import Config
from lattice2d.client import ClientCore
from src.server.server_core import ServerCore
from src.client.menu_states import SplashState, CreatePlayerState, MainMenuState, CreateGameState, GameListState
from lattice2d.command import Command
from config import CONFIG
import sys

class TestMenu():
	class TestSplashState():
		def test_starts_in_splash_state(self, create_client_core):
			client_core = create_client_core()
			assert helpers.is_state(client_core, SplashState)

		def test_transitions_to_create_player_state (self, create_client_core):
			client_core = create_client_core()
			helpers.click_button(client_core, 'begin_button')
			assert helpers.is_state(client_core, CreatePlayerState)

	class TestCreatePlayerState():
		class TestExitButton():
			def test_exits_when_clicked(self, mocker, create_client_core):
				client_core = create_client_core()
				mocker.patch('sys.exit')
				helpers.to_menu_create_player_state(client_core)
				helpers.click_button(client_core, 'exit_button')
				sys.exit.assert_called_once()

		class TestNameInput():
			def test_does_not_send_command_if_player_name_is_too_short(self, mocker, create_client_core):
				client_core = create_client_core()
				mocker.patch.object(client_core, 'add_command')
				helpers.to_menu_create_player_state(client_core)
				helpers.enter_text(client_core, 'name_input', '12345')
				helpers.click_button(client_core, 'continue_button')
				assert not client_core.command_queue.has_elements()

			def test_truncates_player_name_if_player_name_is_too_long(self, create_client_core):
				client_core = create_client_core()
				helpers.to_menu_create_player_state(client_core)
				helpers.enter_text(client_core, 'name_input', '123456789012345678901234567890')
				assert len(helpers.get_text(client_core, 'name_input')) == 23

			def test_sends_command_if_player_name_is_appropriate_length(self, mocker, get_positional_args, create_client_core):
				client_core = create_client_core()
				helpers.to_menu_create_player_state(client_core)
				helpers.enter_text(client_core, 'name_input', '1234567890')
				mocker.patch.object(client_core.current_state, 'add_command')
				helpers.click_button(client_core, 'continue_button')
				command = get_positional_args(client_core.current_state.add_command, 0, 0)
				assert command.type == 'create_player'

		class TestNameInputResponse():
			def test_does_not_transition_if_status_is_not_success(self, mocker, create_client_core):
				client_core = create_client_core()
				helpers.to_menu_create_player_state(client_core)
				helpers.add_command(client_core, Command('create_player', { 'player_name': 'player1' }, 'invalid_name'))
				assert helpers.is_state(client_core, CreatePlayerState)

			def test_transitions_if_status_is_success(self, mocker, create_client_core):
				client_core = create_client_core()
				helpers.to_menu_create_player_state(client_core)
				helpers.add_command(client_core, Command('create_player', { 'player_name': 'player1' }, 'success'))
				assert helpers.is_state(client_core, MainMenuState)

	class TestMainMenuState():
		def test_sends_command_if_exit_is_clicked(self, mocker, get_positional_args, create_client_core):
			client_core = create_client_core()
			helpers.to_menu_main_menu_state(client_core)
			mocker.patch.object(client_core.current_state, 'add_command')
			helpers.click_button(client_core, 'exit_button')
			command = get_positional_args(client_core.current_state.add_command, 0, 0)
			assert command.type == 'logout'

		def test_exits_if_logout_is_successful(self, mocker, create_client_core):
			client_core = create_client_core()
			mocker.patch('sys.exit')
			helpers.to_menu_main_menu_state(client_core)
			helpers.add_command(client_core, Command('logout', {}, 'success'))
			sys.exit.assert_called()

		def test_does_not_exit_if_logout_is_unsuccessful(self, mocker, create_client_core):
			client_core = create_client_core()
			mocker.patch('sys.exit')
			helpers.to_menu_main_menu_state(client_core)
			helpers.add_command(client_core, Command('logout', {}, 'unsuccess'))
			sys.exit.assert_not_called()

		def test_transitions_if_create_game_button_is_clicked(self, mocker, create_client_core):
			client_core = create_client_core()
			helpers.to_menu_main_menu_state(client_core)
			helpers.click_button(client_core, 'create_button')
			assert helpers.is_state(client_core, CreateGameState)

		def test_transitions_if_join_game_button_is_clicked(self, mocker, create_client_core):
			client_core = create_client_core()
			helpers.to_menu_main_menu_state(client_core)
			helpers.click_button(client_core, 'join_button')
			assert helpers.is_state(client_core, GameListState)
