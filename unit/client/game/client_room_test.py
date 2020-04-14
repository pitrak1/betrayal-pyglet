import pytest
import pyglet
from src.client.game import client_room
from src.common import command, bounds
import types
import config

class TestClientRoom():
	class TestAddPlayer():
		def test_adds_player_to_players(self, mocker, create_player):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			player = create_player(mocker, 'player0')
			room.add_player(player)
			assert room.players == [player]

		def test_adjusts_player_positions(self, mocker, create_player):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			mocker.patch.object(room, 'adjust_player_positions')
			player = create_player(mocker, 'player0')
			room.add_player(player)
			room.adjust_player_positions.assert_called_once()

	class TestAdjustPlayerPositions():
		def test_places_one_player(self, mocker, create_player):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			player = create_player(mocker, 'player0')
			room.players.append(player)
			room.adjust_player_positions()
			player.set_position.assert_called_once_with(0, 0, 0, 0, 1.0)

		def test_places_two_players(self, mocker, create_player):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			player0 = create_player(mocker, 'player0')
			room.players.append(player0)
			player1 = create_player(mocker, 'player1')
			room.players.append(player1)
			room.adjust_player_positions()
			player0.set_position.assert_called_once_with(0, 0, -100, 0, 1.0)
			player1.set_position.assert_called_once_with(0, 0, 100, 0, 1.0)

		def test_places_more_than_two_players(self, mocker, create_player):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			player0 = create_player(mocker, 'player0')
			room.players.append(player0)
			player1 = create_player(mocker, 'player1')
			room.players.append(player1)
			player2 = create_player(mocker, 'player2')
			room.players.append(player2)
			room.adjust_player_positions()
			player0.set_position.assert_called_once_with(0, 0, -100, -100, 1.0)
			player1.set_position.assert_called_once_with(0, 0, 100, -100, 1.0)
			player2.set_position.assert_called_once_with(0, 0, -100, 100, 1.0)

	class TestClientMousePressHandler():
		class TestWithoutBounds():
			def test_returns_false(self, mocker, create_state):
				room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
				mocker.patch('src.common.bounds.within_square_bounds', return_value=False)
				state = create_state(mocker)
				command_ = command.Command('client_mouse_press_handler', { 'x': 0, 'y': 0, 'button': pyglet.window.mouse.LEFT })
				assert not room.client_mouse_press_handler(command_, state)
		
		class TestWithinBounds():
			class TestWhenLMB():
				class TestWhenHandledByDefault():
					def test_returns_true(self, mocker, create_state):
						room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
						mocker.patch('src.common.bounds.within_square_bounds', return_value=True)
						mocker.patch.object(room, 'default_handler', return_value=True)
						state = create_state(mocker)
						command_ = command.Command('client_mouse_press_handler', { 'x': 0, 'y': 0, 'button': pyglet.window.mouse.LEFT })
						assert room.client_mouse_press_handler(command_, state)

				class TestWhenNotHandledByDefault():
					def test_returns_true(self, mocker, create_state):
						room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
						mocker.patch('src.common.bounds.within_square_bounds', return_value=True)
						mocker.patch.object(room, 'default_handler', return_value=False)
						state = create_state(mocker)
						command_ = command.Command('client_mouse_press_handler', { 'x': 0, 'y': 0, 'button': pyglet.window.mouse.LEFT })
						assert room.client_mouse_press_handler(command_, state)

					def test_selects(self, mocker, create_state):
						room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
						mocker.patch('src.common.bounds.within_square_bounds', return_value=True)
						mocker.patch.object(room, 'default_handler', return_value=False)
						state = create_state(mocker)
						command_ = command.Command('client_mouse_press_handler', { 'x': 0, 'y': 0, 'button': pyglet.window.mouse.LEFT })
						room.client_mouse_press_handler(command_, state)
						state.select.assert_called_once_with(room)

	class TestClientSelectHandler():
		def test_sets_selected_if_selected(self, mocker):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			command_ = command.Command('client_select_handler', { 'selected': room })
			room.client_select_handler(command_)
			assert room.selected

		def test_resets_selected_if_not_selected(self, mocker):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			command_ = command.Command('client_select_handler', { 'selected': 'not room' })
			room.client_select_handler(command_)
			assert not room.selected

		def test_calls_default_handler(self, mocker):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			command_ = command.Command('client_select_handler', { 'selected': 'not room' })
			mocker.patch.object(room, 'default_handler')
			room.client_select_handler(command_)
			room.default_handler.assert_called_once()

	class TestDefaultHandler():
		def test_calls_on_command_for_players(self, mocker, create_player):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			player0 = create_player(mocker, 'player0')
			player0.on_command = mocker.stub()
			room.players.append(player0)
			player1 = create_player(mocker, 'player1')
			player1.on_command = mocker.stub()
			room.players.append(player1)
			room.default_handler('command', 'state')
			player0.on_command.assert_called_once_with('command', 'state')
			player1.on_command.assert_called_once_with('command', 'state')

		def test_returns_true_if_any_call_returns_true(self, mocker, create_player):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			player0 = create_player(mocker, 'player0')
			player0.on_command = lambda command, state : True
			room.players.append(player0)
			player1 = create_player(mocker, 'player1')
			player1.on_command = lambda command, state : False
			room.players.append(player1)
			assert room.default_handler('command', 'state')

		def test_returns_false_if_all_calls_return_false(self, mocker, create_player):
			room = client_room.ClientRoom(config.STARTING_ROOMS[0], testing=True)
			player0 = create_player(mocker, 'player0')
			player0.on_command = lambda command, state : False
			room.players.append(player0)
			player1 = create_player(mocker, 'player1')
			player1.on_command = lambda command, state : False
			room.players.append(player1)
			assert not room.default_handler('command', 'state')

