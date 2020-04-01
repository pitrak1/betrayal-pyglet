import pytest
import pyglet
import sys
from src.client.states.menu import game_list_state, main_menu_state, game_state
import config
from src.shared import constants
import types

class TestGameListState():
	def test_adds_network_get_games_on_creation(self, mocker, get_args):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_get_games'

	def test_sets_games_info_on_set_games(self, mocker):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		games = ['game_1', 'game_2', 'game_3', 'game_4']
		state.set_games(games)
		assert state.available_games == games
		assert state.available_games_count == 4

	def test_increments_current_page_on_go_forward_page(self, mocker):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.go_forward_page()
		assert state.current_page == 1

	def test_decrements_current_page_on_go_back_page(self, mocker):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.go_back_page()
		assert state.current_page == -1

	def test_adds_network_get_games_on_refresh(self, mocker, get_args):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.refresh()
		assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_get_games'

	def test_sets_state_to_main_menu_state_on_back_click(self, mocker, get_args):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.back()
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), main_menu_state.MainMenuState)

	def test_sets_error_text_if_join_with_too_many_players(self, mocker):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		error_text = types.SimpleNamespace()
		error_text.text = ''
		state.elements = { 'error_text': error_text }
		state.join('game_name', constants.PLAYERS_PER_GAME + 1)
		assert state.elements['error_text'].text == 'Game is full'

	def test_adds_network_join_game_on_join(self, mocker, get_args):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.join('game_name', constants.PLAYERS_PER_GAME - 1)
		assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_join_game'

	def test_sets_error_text_on_game_full(self, mocker):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		error_text = types.SimpleNamespace()
		error_text.text = ''
		state.elements = { 'error_text': error_text }
		state.game_full()
		assert state.elements['error_text'].text == 'Game is full'

	def test_sets_state_to_game_state_on_next(self, mocker, get_args):
		state = game_list_state.GameListState({}, mocker.stub(), mocker.stub(), 'player_name', testing=True)
		state.next('game_name')
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), game_state.GameState)
