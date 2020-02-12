import pytest
import types
from src.world import world_node, room_node, character_node
from src.state import state_machine

@pytest.fixture
def make_world_node(make_state_machine):
	def _make_world_node(mocker):
		mocker.patch('pyglet.sprite.Sprite')
		return world_node.WorldNode(make_state_machine(mocker))
	return _make_world_node

@pytest.fixture
def make_world_node_with_stubbed_rooms(make_state_machine, make_stubbed_room_node):
	def _make_world_node_with_stubbed_rooms(mocker):
		node = world_node.WorldNode(make_state_machine(mocker))
		node.rooms[1][2] = make_stubbed_room_node(mocker)
		node.rooms[2][3] = make_stubbed_room_node(mocker)
		return node
	return _make_world_node_with_stubbed_rooms

@pytest.fixture
def make_state_machine(make_list):
	def _make_state_machine(mocker):
		return state_machine.StateMachine(make_list(mocker))
	return _make_state_machine

@pytest.fixture
def make_stubbed_state_machine(make_state_machine):
	def _make_stubbed_state_machine(mocker):
		state_machine = make_state_machine(mocker)
		mocker.patch.object(state_machine, 'select')
		return state_machine
	return _make_stubbed_state_machine

@pytest.fixture
def make_list():
	def _make_list(mocker):
		stubbed_list = types.SimpleNamespace()
		stubbed_list.append = mocker.stub()
		return stubbed_list
	return _make_list

@pytest.fixture
def make_sprite():
	def _make_sprite(mocker, x=5, y=10, rotation=0.0, scale_x=1.0, scale_y=1.0):
		sprite = types.SimpleNamespace()
		sprite.update = mocker.stub()
		sprite.draw = mocker.stub()
		sprite.x = x
		sprite.y = y
		sprite.rotation = rotation
		sprite.scale_x = scale_x
		sprite.scale_y = scale_y
		return sprite
	return _make_sprite

@pytest.fixture
def make_room_node(make_stubbed_state_machine, make_sprite):
	def _make_room_node(mocker, grid_x=0, grid_y=0):
		mocker.patch('pyglet.sprite.Sprite')
		node = room_node.RoomNode(img='image', img_selected='image', grid_x=grid_x, grid_y=grid_y, state_machine=make_stubbed_state_machine(mocker))
		node.sprite = make_sprite(mocker, x=grid_x * room_node.ROOM_SIZE, y=grid_y * room_node.ROOM_SIZE)
		node.sprite_selected = make_sprite(mocker, x=grid_x * room_node.ROOM_SIZE, y=grid_y * room_node.ROOM_SIZE)
		return node
	return _make_room_node

@pytest.fixture
def make_stubbed_room_node(make_room_node):
	def _make_stubbed_room_node(mocker):
		node = make_room_node(mocker)
		mocker.patch.object(node, 'on_command')
		mocker.patch.object(node, 'on_update')
		mocker.patch.object(node, 'on_draw')
		return node
	return _make_stubbed_room_node

@pytest.fixture
def make_room_node_with_stubbed_characters(make_room_node, make_stubbed_character_node):
	def _make_room_node_with_stubbed_characters(mocker, grid_x=0, grid_y=0):
		node = make_room_node(mocker, grid_x, grid_y)
		node.characters.append(make_stubbed_character_node(mocker))
		node.characters.append(make_stubbed_character_node(mocker))
		return node
	return _make_room_node_with_stubbed_characters

@pytest.fixture
def make_character_node(make_stubbed_state_machine, make_sprite):
	def _make_character_node(mocker, x=0, y=0):
		mocker.patch('pyglet.sprite.Sprite')
		node = character_node.CharacterNode(img='image', img_selected='image', grid_x=0, grid_y=0, x=x, y=y, state_machine=make_stubbed_state_machine(mocker))
		node.sprite = make_sprite(mocker, x=x, y=y)
		node.sprite_selected = make_sprite(mocker, x=x, y=y)
		return node
	return _make_character_node

@pytest.fixture
def make_stubbed_character_node(make_character_node):
	def _make_stubbed_character_node(mocker):
		node = make_character_node(mocker)
		mocker.patch.object(node, 'on_command')
		mocker.patch.object(node, 'on_update')
		mocker.patch.object(node, 'on_draw')
		return node
	return _make_stubbed_character_node
