import pytest
import pyglet
from src.client.game import client_player
from src.common import command, bounds
import types
import config

class TestClientPlayer():
	class TestClientMousePressHandler():
		class TestWhenWithoutBounds():
			def test_returns_false(self, mocker, create_state):
				player = client_player.ClientPlayer(config.CHARACTERS[0], 'player0', False, True, testing=True)
				mocker.patch('src.common.bounds.within_circle_bounds', return_value=False)
				state = create_state(mocker)
				command_ = command.Command('client_mouse_press_handler', { 'x': 0, 'y': 0, 'button': pyglet.window.mouse.LEFT })
				assert not player.client_mouse_press_handler(command_, state)
		
		class TestWhenWithinBounds():
			class TestWhenLMB():
				def test_selects(self, mocker, create_state):
					player = client_player.ClientPlayer(config.CHARACTERS[0], 'player0', False, True, testing=True)
					mocker.patch('src.common.bounds.within_circle_bounds', return_value=True)
					state = create_state(mocker)
					command_ = command.Command('client_mouse_press_handler', { 'x': 0, 'y': 0, 'button': pyglet.window.mouse.LEFT })
					player.client_mouse_press_handler(command_, state)
					state.select.assert_called_once_with(player)

				def test_returns_true(self, mocker, create_state):
					player = client_player.ClientPlayer(config.CHARACTERS[0], 'player0', False, True, testing=True)
					mocker.patch('src.common.bounds.within_circle_bounds', return_value=True)
					state = create_state(mocker)
					command_ = command.Command('client_mouse_press_handler', { 'x': 0, 'y': 0, 'button': pyglet.window.mouse.LEFT })
					assert player.client_mouse_press_handler(command_, state)

	class TestClientSelectHandler():
		def test_sets_selected_if_selected(self, mocker):
			player = client_player.ClientPlayer(config.CHARACTERS[0], 'player0', False, True, testing=True)
			command_ = command.Command('client_select_handler', { 'selected': player })
			player.client_select_handler(command_)
			assert player.selected

		def test_resets_selected_if_not_selected(self, mocker):
			player = client_player.ClientPlayer(config.CHARACTERS[0], 'player0', False, True, testing=True)
			command_ = command.Command('client_select_handler', { 'selected': 'not player' })
			player.client_select_handler(command_)
			assert not player.selected
