import pytest
import pyglet
from src.world import absolute_node

class TestAbsoluteNode():
	class TestConstructor():
		def test_creates_sprite(self, mocker):
			mocker.patch('pyglet.sprite')
			node = absolute_node.AbsoluteNode(img='image', batch='batch')
			pyglet.sprite.Sprite.assert_called_once_with('image', 0, 0, batch='batch')

		def test_allows_setting_position(self, mocker):
			mocker.patch('pyglet.sprite')
			node = absolute_node.AbsoluteNode(img='image', batch='batch', x=15, y=20)
			pyglet.sprite.Sprite.assert_called_once_with('image', 15, 20, batch='batch')

	class TestOnUpdate():
		def test_calls_on_update_for_children(self, mocker):
			mocker.patch('pyglet.sprite')
			node = absolute_node.AbsoluteNode(img='image', batch='batch')
			child1 = absolute_node.AbsoluteNode(img='image', batch='batch')
			child2 = absolute_node.AbsoluteNode(img='image', batch='batch')
			node.children = [child1, child2]
			mocker.patch.object(child1, 'on_update')
			mocker.patch.object(child2, 'on_update')
			node.on_update(1)
			child1.on_update.assert_called_once_with(1)
			child2.on_update.assert_called_once_with(1)

	class TestSetTransform():
		def test_allows_setting_position_rotation_and_scale(self, mocker):
			mocker.patch('pyglet.sprite')
			node = absolute_node.AbsoluteNode(img='image', batch='batch')
			mocker.patch.object(node.sprite, 'update')
			node.set_transform(15, 20, 30, 1.5, 2.5)
			node.sprite.update.assert_called_once_with(x=15, y=20, rotation=30, scale_x=1.5, scale_y=2.5)

	class TestAddChild():
		def test_allows_adding_children(self, mocker):
			mocker.patch('pyglet.sprite')
			node = absolute_node.AbsoluteNode(img='image', batch='batch')
			child1 = absolute_node.AbsoluteNode(img='image', batch='batch')
			node.add_child(child1)
			assert node.children == [child1]

		def test_sets_parent_of_child(self, mocker):
			mocker.patch('pyglet.sprite')
			node = absolute_node.AbsoluteNode(img='image', batch='batch')
			child1 = absolute_node.AbsoluteNode(img='image', batch='batch')
			node.add_child(child1)
			assert child1.parent == node

    