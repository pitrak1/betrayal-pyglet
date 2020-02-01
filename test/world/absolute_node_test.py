import pytest
import pyglet
from src.world import absolute_node
from pyglet import sprite

class TestAbsoluteNode():
	class TestConstructor():
		def test_creates_sprite(self, mocker, make_absolute_node):
			make_absolute_node(mocker)
			sprite.Sprite.assert_called_once_with('image', 0, 0, batch='batch')

		def test_allows_setting_position(self, mocker, make_absolute_node):
			make_absolute_node(mocker, x=15, y=20)
			sprite.Sprite.assert_called_once_with('image', 15, 20, batch='batch')

	class TestOnCommand():
		def test_calls_on_command_for_children(self, mocker, make_absolute_node_with_children):
			node = make_absolute_node_with_children(mocker)
			node.on_command('command', 'queue')
			node.children[0].on_command.assert_called_once_with('command', 'queue')
			node.children[1].on_command.assert_called_once_with('command', 'queue')

	class TestOnUpdate():
		def test_calls_on_update_for_children(self, mocker, make_absolute_node_with_children):
			node = make_absolute_node_with_children(mocker)
			node.on_update(1)
			node.children[0].on_update.assert_called_once_with(1)
			node.children[1].on_update.assert_called_once_with(1)

	class TestSetTransform():
		def test_allows_setting_position_rotation_and_scale(self, mocker, make_absolute_node):
			node = make_absolute_node(mocker)
			node.set_transform(15, 20, 30, 1.5, 2.5)
			node.sprite.update.assert_called_once_with(x=15, y=20, rotation=30, scale_x=1.5, scale_y=2.5)

	class TestAddChild():
		def test_allows_adding_children(self, mocker, make_absolute_node):
			node = make_absolute_node(mocker)
			child = make_absolute_node(mocker)
			node.add_child(child)
			assert node.children == [child]

		def test_sets_parent_of_child(self, mocker, make_absolute_node):
			node = make_absolute_node(mocker)
			child = make_absolute_node(mocker)
			node.add_child(child)
			assert child.parent == node

    