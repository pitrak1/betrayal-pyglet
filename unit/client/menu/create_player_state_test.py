import pytest
import pyglet
import sys
from src.client.menu import create_player_state, main_menu_state
import config
import types

class TestCreatePlayState():
	class TestExit():
		def test_exits(self, mocker):
			mocker.patch('sys.exit')
			state = create_player_state.CreatePlayerState({}, mocker.stub(), mocker.stub(), testing=True)
			state.exit()
			sys.exit.assert_called_once()

	class TestInvalidPlayerName():
		def test_sets_invalid_player_name_error(self, mocker):
			state = create_player_state.CreatePlayerState({}, mocker.stub(), mocker.stub(), testing=True)
			player_name_input = types.SimpleNamespace()
			player_name_input.set_error_text = mocker.stub()
			state.elements = { 'player_name_input': player_name_input }
			state.invalid_player_name()
			state.elements['player_name_input'].set_error_text.assert_called_once_with('name is already in use')

	class TestNameTooShort():
		def test_sets_error(self, mocker):
			state = create_player_state.CreatePlayerState({}, mocker.stub(), mocker.stub(), testing=True)
			player_name_input = types.SimpleNamespace()
			player_name_input.set_error_text = mocker.stub()
			state.elements = { 'player_name_input': player_name_input }
			state.name_too_short()
			state.elements['player_name_input'].set_error_text.assert_called_once_with('must be 6 characters or more')

	class TestNameTooLong():
		def test_sets_error(self, mocker):
			state = create_player_state.CreatePlayerState({}, mocker.stub(), mocker.stub(), testing=True)
			player_name_input = types.SimpleNamespace()
			player_name_input.set_error_text = mocker.stub()
			state.elements = { 'player_name_input': player_name_input }
			state.name_too_long()
			state.elements['player_name_input'].set_error_text.assert_called_once_with('must be 25 characters or less')

	class TestContinue():
		def test_sets_name_too_short_if_too_short(self, mocker):
			state = create_player_state.CreatePlayerState({}, mocker.stub(), mocker.stub(), testing=True)
			player_name_input = types.SimpleNamespace()
			player_name_input.set_error_text = mocker.stub()
			player_name_input.get_text = lambda : '12345'
			state.elements = { 'player_name_input': player_name_input }
			state.continue_()
			state.elements['player_name_input'].set_error_text.assert_called_once_with('must be 6 characters or more')

		def test_adds_network_create_player_command(self, mocker, get_args):
			state = create_player_state.CreatePlayerState({}, mocker.stub(), mocker.stub(), testing=True)
			player_name_input = types.SimpleNamespace()
			player_name_input.get_text = lambda : '123456'
			state.elements = { 'player_name_input': player_name_input }
			state.continue_()
			assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_create_player'

	class TestNext():
		def test_sets_state_to_main_menu_state(self, mocker, get_args):
			state = create_player_state.CreatePlayerState({}, mocker.stub(), mocker.stub(), testing=True)
			state.next('player_name')
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), main_menu_state.MainMenuState)
