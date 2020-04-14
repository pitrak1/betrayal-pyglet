import pytest
import pyglet
import sys
from src.client.game import game_state
import config
from src.common import constants
import types

class TestGameState():
	class TestConstructor():
		def test_adds_network_get_player_positions(self, mocker, get_args):
			state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_get_player_positions'

	class TestSetPlayerPositions():
		def test_adds_players_to_players(self, mocker, get_args):
			state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.set_player_positions([
				('player0', config.CHARACTERS[0]['variable_name'], 0, 0),
				('player1', config.CHARACTERS[1]['variable_name'], 2, 3),
				('player2', config.CHARACTERS[2]['variable_name'], 4, 5),
			])
			assert len(state.players) == 3

		def test_adds_player_to_room_grid(self, mocker, get_args):
			state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.rooms = types.SimpleNamespace()
			state.rooms.add_player = mocker.stub()
			state.set_player_positions([
				('player0', config.CHARACTERS[0]['variable_name'], 0, 0),
				('player1', config.CHARACTERS[1]['variable_name'], 2, 3),
				('player2', config.CHARACTERS[2]['variable_name'], 4, 5),
			])
			assert state.rooms.add_player.call_count == 3

		def test_adds_network_get_current_player(self, mocker, get_args):
			state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.rooms = types.SimpleNamespace()
			state.rooms.add_player = mocker.stub()
			state.set_player_positions([
				('player0', config.CHARACTERS[0]['variable_name'], 0, 0),
				('player1', config.CHARACTERS[1]['variable_name'], 2, 3),
				('player2', config.CHARACTERS[2]['variable_name'], 4, 5),
			])
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_get_current_player'

	class TestSetCurrentPlayer():
		class TestWithSelf():
			def test_sets_title(self, mocker):
				state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
				state.set_current_player('self')
				assert state.title == 'Your turn'

			def test_sets_current_player_to_true(self, mocker):
				state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
				state.set_current_player('self')
				assert state.current_player

		class TestWithOtherThanSelf():
			def test_sets_title(self, mocker):
				state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
				state.set_current_player('player0')
				assert state.title == 'player0\'s turn'

			def test_sets_current_player_to_false(self, mocker):
				state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
				state.set_current_player('player0')
				assert not state.current_player

		def test_adds_client_redraw(self, mocker, get_args):
			state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.set_current_player('self')
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'client_redraw'

	class TestSelect():
		def test_sets_selected(self, mocker):
			state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.select('node')
			assert state.selected == 'node'

		def test_adds_client_select(self, mocker, get_args):
			state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.select('node')
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'client_select'

		def test_adds_client_redraw(self, mocker, get_args):
			state = game_state.GameState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.select('node')
			assert get_args(state.add_command, call_number=2, arg_number=0).type == 'client_redraw'
