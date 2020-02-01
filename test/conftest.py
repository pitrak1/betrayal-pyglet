import pytest
import types
from src.world import absolute_node, relative_node

@pytest.fixture
def make_sprite():
	def _make_sprite(mocker, x=5, y=10, rotation=0.0, scale_x=1.0, scale_y=1.0):
		sprite = types.SimpleNamespace()
		sprite.update = mocker.stub()
		sprite.x = x
		sprite.y = y
		sprite.rotation = rotation
		sprite.scale_x = scale_x
		sprite.scale_y = scale_y
		return sprite
	return _make_sprite

@pytest.fixture
def make_absolute_node(make_sprite):
	def _make_absolute_node(mocker, x=0, y=0):
		mocker.patch('pyglet.sprite.Sprite')
		node = absolute_node.AbsoluteNode(img='image', batch='batch', x=x, y=y)
		node.sprite = make_sprite(mocker, x=x, y=y)
		return node
	return _make_absolute_node

@pytest.fixture
def make_stubbed_absolute_node(make_absolute_node):
	def _make_stubbed_absolute_node(mocker):
		node = make_absolute_node(mocker)
		mocker.patch.object(node, 'on_command')
		mocker.patch.object(node, 'on_update')
		return node
	return _make_stubbed_absolute_node

@pytest.fixture
def make_absolute_node_with_children(make_absolute_node, make_stubbed_absolute_node):
	def _make_absolute_node_with_children(mocker):
		node = make_absolute_node(mocker)
		child1 = make_stubbed_absolute_node(mocker)
		child2 = make_stubbed_absolute_node(mocker)
		node.children = [child1, child2]
		return node
	return _make_absolute_node_with_children

@pytest.fixture
def make_relative_node(make_absolute_node, make_sprite):
	def _make_relative_node(mocker, parent_x=0, parent_y=0, x=0, y=0):
		parent = make_absolute_node(mocker, x=parent_x, y=parent_y)
		node = relative_node.RelativeNode(img='image', batch='batch')
		node.relative_x = x
		node.relative_y = y
		node.sprite = make_sprite(mocker)
		parent.children.append(node)
		node.parent = parent
		return node
	return _make_relative_node

@pytest.fixture
def make_stubbed_relative_node(make_relative_node):
	def _make_stubbed_relative_node(mocker):
		node = make_relative_node(mocker)
		mocker.patch.object(node, 'on_command')
		mocker.patch.object(node, 'on_update')
		return node
	return _make_stubbed_relative_node

@pytest.fixture
def make_relative_node_with_children(make_absolute_node, make_relative_node, make_stubbed_relative_node):
	def _make_relative_node_with_children(mocker):
		parent = make_absolute_node(mocker)
		node = make_relative_node(mocker)
		parent.children.append(node)
		node.parent = parent
		child1 = make_stubbed_relative_node(mocker)
		child2 = make_stubbed_relative_node(mocker)
		node.children = [child1, child2]
		return node
	return _make_relative_node_with_children


