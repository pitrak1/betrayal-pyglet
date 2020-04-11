import pytest
import pyglet
from src.client import client_game
from src.common import command
import types

class TestGame():
	class TestSetState():
		def test_sets_current_state(self, mocker):
			game_ = client_game.Game(testing=True)
			game_.set_state('some state')
			assert game_.current_state == 'some state'

	class TestOnKeyPress():
		def test_adds_client_key_press_command(self, mocker):
			game_ = client_game.Game(testing=True)
			game_.on_key_press('symbol', 'modifiers')
			assert game_.command_queue.pop_front().type == 'client_key_press'

	class TestOnText():
		def test_adds_client_text_entered_command(self, mocker):
			game_ = client_game.Game(testing=True)
			game_.on_text('text')
			assert game_.command_queue.pop_front().type == 'client_text_entered'

	class TestOnTextMotion():
		def test_adds_client_text_motion_command(self, mocker):
			game_ = client_game.Game(testing=True)
			game_.on_text_motion('motion')
			assert game_.command_queue.pop_front().type == 'client_text_motion'

	class TestOnTextMotionSelect():
		def test_adds_client_text_motion_select_command(self, mocker):
			game_ = client_game.Game(testing=True)
			game_.on_text_motion_select('motion')
			assert game_.command_queue.pop_front().type == 'client_text_motion_select'

	class TestOnMousePress():
		def test_adds_client_mouse_press_command(self, mocker):
			game_ = client_game.Game(testing=True)
			game_.on_mouse_press('x', 'y', 'button', 'modifiers')
			assert game_.command_queue.pop_front().type == 'client_mouse_press'

	class TestOnMouseDrag():
		def test_adds_client_mouse_drag_command(self, mocker):
			game_ = client_game.Game(testing=True)
			game_.on_mouse_drag('x', 'y', 'dx', 'dy', 'buttons', 'modifiers')
			assert game_.command_queue.pop_front().type == 'client_mouse_drag'

	class TestOnMouseScroll():
		def test_adds_client_mouse_scroll_command(self, mocker):
			game_ = client_game.Game(testing=True)
			game_.on_mouse_scroll('x', 'y', 'dx', 'dy')
			assert game_.command_queue.pop_front().type == 'client_mouse_scroll'
