import pytest
import pyglet
import sys
from src.client.states.menu import main_menu_state, create_game_state, game_list_state
import config

class TestMainMenuState():
	def test_adds_network_logout_on_exit_click(self, mocker, get_args):
		state = main_menu_state.MainMenuState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.start_exit()
		assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_logout'

	def test_exits_on_exit_click(self, mocker):
		mocker.patch('sys.exit')
		state = main_menu_state.MainMenuState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.exit()
		sys.exit.assert_called_once()

	def test_sets_state_to_create_game_state_on_create_game(self, mocker, get_args):
		state = main_menu_state.MainMenuState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.create_game()
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), create_game_state.CreateGameState)

	def test_sets_state_to_game_list_state_on_join_game(self, mocker, get_args):
		state = main_menu_state.MainMenuState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.join_game()
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), game_list_state.GameListState)
