import pytest
import pyglet
from src import node as node_module
from src.states import commands as  commands_module

class TestNode():
	class TestOnDraw():
		def test_raises_exception(self):
			node = node_module.Node()
			with pytest.raises(NotImplementedError) as exception:
				node.on_draw('state')
			assert str(exception.value) == 'on_draw must be overridden'

	class TestOnCommand():
		def test_calls_mouse_press_handler_on_command(self, mocker):
			node = node_module.Node()
			mocker.patch.object(node, 'mouse_press_handler')
			command = commands_module.MousePressCommand('position', 'button', 'modifiers')
			node.on_command(command, 'state')
			node.mouse_press_handler.assert_called_once_with(command, 'state')

		def test_calls_key_press_handler_on_command(self, mocker):
			node = node_module.Node()
			mocker.patch.object(node, 'key_press_handler')
			command = commands_module.KeyPressCommand('symbol', 'modifiers')
			node.on_command(command, 'state')
			node.key_press_handler.assert_called_once_with(command, 'state')

		def test_calls_add_room_handler_on_command(self, mocker):
			node = node_module.Node()
			mocker.patch.object(node, 'add_room_handler')
			command = commands_module.AddRoomCommand('room_tile', 'grid_position', 'rotation')
			node.on_command(command, 'state')
			node.add_room_handler.assert_called_once_with(command, 'state')

		def test_calls_add_character_handler_on_command(self, mocker):
			node = node_module.Node()
			mocker.patch.object(node, 'add_character_handler')
			command = commands_module.AddCharacterCommand('character_tile', 'grid_position')
			node.on_command(command, 'state')
			node.add_character_handler.assert_called_once_with(command, 'state')

		def test_calls_move_character_handler_on_command(self, mocker):
			node = node_module.Node()
			mocker.patch.object(node, 'move_character_handler')
			command = commands_module.MoveCharacterCommand('character', 'grid_position')
			node.on_command(command, 'state')
			node.move_character_handler.assert_called_once_with(command, 'state')

	class TestDefaultHandler():
		def test_raises_exception(self):
			node = node_module.Node()
			with pytest.raises(NotImplementedError) as exception:
				node.default_handler('command', 'state')
			assert str(exception.value) == 'default_handler must be overridden'

	class TestOnUpdate():
		def test_raises_exception(self):
			node = node_module.Node()
			with pytest.raises(NotImplementedError) as exception:
				node.on_update('dt', 'state')
			assert str(exception.value) == 'on_update must be overridden'