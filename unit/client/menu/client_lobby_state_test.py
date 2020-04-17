import pytest
import pyglet
import sys
from src.client.menu import main_menu_state, client_lobby_state
from src.client.setup import player_order_state
import config
from src.common import constants
import types

class TestClientLobbyState():
	class TestConstructor():
		def test_adds_network_get_games(self, mocker, get_args):
			state = client_lobby_state.ClientLobbyState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_get_players_in_game'

	class TestLeaveGame():
		def test_adds_network_leave_game(self, mocker, get_args):	
			state = client_lobby_state.ClientLobbyState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.leave_game()
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_leave_game'

	class TestBack():
		def test_sets_state_to_main_menu_state(self, mocker, get_args):
			state = client_lobby_state.ClientLobbyState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.back()
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), main_menu_state.MainMenuState)

	class TestStartGame():
		def test_sets_error_text_if_not_enough_players(self, mocker):
			state = client_lobby_state.ClientLobbyState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			error_text = types.SimpleNamespace()
			error_text.text = ''
			state.elements = { 'error_text': error_text }
			state.players = ['player1']
			state.start_game()
			assert state.elements['error_text'].text == 'Two or more players are required'

		def test_adds_network_start_game(self, mocker, get_args):
			state = client_lobby_state.ClientLobbyState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.players = ['player1', 'player2']
			state.start_game()
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_start_game'

	class TestNotEnoughPlayers():
		def test_sets_error_text(self, mocker):
			state = client_lobby_state.ClientLobbyState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			error_text = types.SimpleNamespace()
			error_text.text = ''
			state.elements = { 'error_text': error_text }
			state.not_enough_players()
			assert state.elements['error_text'].text == 'Two or more players are required'

	class TestNext():
		def test_sets_state_to_client_lobby_state(self, mocker, get_args):
			state = client_lobby_state.ClientLobbyState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.next()
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), player_order_state.PlayerOrderState)
