import pytest
import pyglet
import sys
from src.client.menu import main_menu_state, create_game_state, game_state
import config
import types

class TestCreateGameState():
	class TestBack():
		def test_sets_state_to_main_menu_state(self, mocker, get_args):
			state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			state.back()
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), main_menu_state.MainMenuState)

	class TestInvalidGameName():
		def test_sets_error(self, mocker):
			state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			game_name_input = types.SimpleNamespace()
			game_name_input.set_error_text = mocker.stub()
			state.elements = { 'game_name_input': game_name_input }
			state.invalid_game_name()
			state.elements['game_name_input'].set_error_text.assert_called_once_with('name is already in use')

	class TestNameTooShort():
		def test_sets_error(self, mocker):
			state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			game_name_input = types.SimpleNamespace()
			game_name_input.set_error_text = mocker.stub()
			state.elements = { 'game_name_input': game_name_input }
			state.name_too_short()
			state.elements['game_name_input'].set_error_text.assert_called_once_with('must be 6 characters or more')

	class TestNameTooLong():
		def test_sets_error(self, mocker):
			state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			game_name_input = types.SimpleNamespace()
			game_name_input.set_error_text = mocker.stub()
			state.elements = { 'game_name_input': game_name_input }
			state.name_too_long()
			state.elements['game_name_input'].set_error_text.assert_called_once_with('must be 40 characters or less')

	class TestCreate():
		def test_sets_name_too_short_if_too_short(self, mocker):
			state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			game_name_input = types.SimpleNamespace()
			game_name_input.set_error_text = mocker.stub()
			game_name_input.get_text = lambda : '12345'
			state.elements = { 'game_name_input': game_name_input }
			state.create()
			state.elements['game_name_input'].set_error_text.assert_called_once_with('must be 6 characters or more')

		def test_adds_network_create_game_command(self, mocker, get_args):
			state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			game_name_input = types.SimpleNamespace()
			game_name_input.get_text = lambda : '123456'
			state.elements = { 'game_name_input': game_name_input }
			state.create()
			assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_create_game'

	class TestNext():
		def test_sets_state_to_game_state(self, mocker, get_args):
			state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			state.next('game_name')
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), game_state.GameState)
