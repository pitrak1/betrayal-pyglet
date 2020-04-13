import pytest
import pyglet
import sys
from src.client.menu import main_menu_state, create_game_state, game_state
import config
import types

class TestCreateGameState():
	def test_sets_state_to_main_menu_state_on_back_click(self, mocker, get_args):
		state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.back()
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), main_menu_state.MainMenuState)

	def test_sets_invalid_game_name_error(self, mocker):
		state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		game_name_input = types.SimpleNamespace()
		game_name_input.set_error_text = mocker.stub()
		state.elements = { 'game_name_input': game_name_input }
		state.invalid_game_name()
		state.elements['game_name_input'].set_error_text.assert_called_once_with('name is already in use')

	def test_sets_name_too_short_error(self, mocker):
		state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		game_name_input = types.SimpleNamespace()
		game_name_input.set_error_text = mocker.stub()
		state.elements = { 'game_name_input': game_name_input }
		state.name_too_short()
		state.elements['game_name_input'].set_error_text.assert_called_once_with('must be 6 characters or more')

	def test_sets_name_too_long_error(self, mocker):
		state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		game_name_input = types.SimpleNamespace()
		game_name_input.set_error_text = mocker.stub()
		state.elements = { 'game_name_input': game_name_input }
		state.name_too_long()
		state.elements['game_name_input'].set_error_text.assert_called_once_with('must be 40 characters or less')

	def test_sets_name_too_short_if_too_short_on_create_click(self, mocker):
		state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		game_name_input = types.SimpleNamespace()
		game_name_input.set_error_text = mocker.stub()
		game_name_input.get_text = lambda : '12345'
		state.elements = { 'game_name_input': game_name_input }
		state.create()
		state.elements['game_name_input'].set_error_text.assert_called_once_with('must be 6 characters or more')

	def test_adds_network_create_game_command_on_create_click(self, mocker, get_args):
		state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		game_name_input = types.SimpleNamespace()
		game_name_input.get_text = lambda : '123456'
		state.elements = { 'game_name_input': game_name_input }
		state.create()
		assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_create_game'

	def test_sets_state_to_game_state_on_next(self, mocker, get_args):
		state = create_game_state.CreateGameState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.next('game_name')
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), game_state.GameState)
