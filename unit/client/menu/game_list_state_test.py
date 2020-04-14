import pytest
import pyglet
import sys
from src.client.menu import game_list_state, main_menu_state, game_state
import config
from src.common import constants
import types

class TestGameListState():
	class TestConstructor():
		def test_adds_network_get_games(self, mocker, get_args):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_get_games'

	class TestSetGames():
		def test_sets_games_info(self, mocker):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			games = ['game_1', 'game_2', 'game_3', 'game_4']
			state.set_games(games)
			assert state.available_games == games
			assert state.available_games_count == 4

	class TestGoForwardPage():
		def test_increments_current_page(self, mocker):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			state.go_forward_page()
			assert state.current_page == 1

	class TestGoBackPage():
		def test_decrements_current_page(self, mocker):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			state.go_back_page()
			assert state.current_page == -1

	class TestRefresh():
		def test_adds_network_get_games(self, mocker, get_args):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			state.refresh()
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_get_games'

	class TestBack():
		def test_sets_state_to_main_menu_state(self, mocker, get_args):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			state.back()
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), main_menu_state.MainMenuState)

	class TestJoin():
		def test_sets_error_text_if_too_many_players(self, mocker):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			error_text = types.SimpleNamespace()
			error_text.text = ''
			state.elements = { 'error_text': error_text }
			state.join('game_name', constants.PLAYERS_PER_GAME + 1)
			assert state.elements['error_text'].text == 'Game is full'

		def test_adds_network_join_game(self, mocker, get_args):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			state.join('game_name', constants.PLAYERS_PER_GAME - 1)
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_join_game'

	class TestGameFull():
		def test_sets_error_text(self, mocker):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			error_text = types.SimpleNamespace()
			error_text.text = ''
			state.elements = { 'error_text': error_text }
			state.game_full()
			assert state.elements['error_text'].text == 'Game is full'

	class TestNext():
		def test_sets_state_to_game_state(self, mocker, get_args):
			state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
			state.next('game_name')
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), game_state.GameState)
