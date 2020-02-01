import pytest
import pyglet
from src.world import absolute_node, relative_node
from pyglet import sprite
import types

class TestRelativeNode():
	class TestOnCommand():
		def test_updates_transform(self, mocker, make_relative_node):
			node = make_relative_node(mocker)
			node.on_command('command', 'queue')
			node.sprite.update.assert_called_once()

		def test_calls_on_command_for_children(self, mocker, make_relative_node_with_children):
			node = make_relative_node_with_children(mocker)
			node.on_command('command', 'queue')
			node.children[0].on_command.assert_called_once_with('command', 'queue')
			node.children[1].on_command.assert_called_once_with('command', 'queue')

	class TestOnUpdate():
		def test_updates_transform(self, mocker, make_relative_node):
			node = make_relative_node(mocker)
			node.on_update('dt')
			node.sprite.update.assert_called_once()

		def test_calls_on_command_for_children(self, mocker, make_relative_node_with_children):
			node = make_relative_node_with_children(mocker)
			node.on_update('dt')
			node.children[0].on_update.assert_called_once_with('dt')
			node.children[1].on_update.assert_called_once_with('dt')

	class TestUpdateTransform():
		def test_combines_transform_with_transform_of_parent(self, mocker, make_relative_node):
			node = make_relative_node(mocker, parent_x=15, parent_y=20, x=5, y=10)
			node.update_transform()
			node.sprite.update.assert_called_once_with(x=20, y=30, rotation=0.0, scale_x=1.0, scale_y=1.0)

	class TestUpdateRelativeTransform():
		def test_sets_relative_transform_values(self, mocker, make_relative_node):
			node = make_relative_node(mocker, parent_x=15, parent_y=20, x=5, y=10)
			node.set_relative_transform(x=30, y=35)
			assert node.relative_x == 30
			assert node.relative_y == 35

		def test_updates_transform(self, mocker, make_relative_node):
			node = make_relative_node(mocker)
			node.set_relative_transform(x=30, y=35)
			node.sprite.update.assert_called_once()
    