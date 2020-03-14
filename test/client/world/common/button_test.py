import pytest
import pyglet
from src.client.world.common import button as button_module
from src.shared import command as command_module

class TestButton():
	class TestClientTranslatedMousePressHandler():
		def test_calls_on_click_if_within_bounds(self, mocker):
			mocker.patch('pyglet.sprite')
			callback = mocker.stub()
			button = button_module.Button(range(9), 0, 0, 3, 5, 'Some Text', callback)
			command = command_module.Command('client_translated_mouse_press', { 'x': 0, 'y': 0 })
			button.on_command(command)
			callback.assert_called_once()
