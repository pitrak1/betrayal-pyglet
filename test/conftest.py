import pytest
import types
import config

pytest_plugins = [
	# 'fixtures.nodes.character_node_fixture',
	# 'fixtures.nodes.world_node_fixture',
	# 'fixtures.states.selected_state_fixture',
	# 'fixtures.tiles.character_tile_fixture',
	# 'fixtures.tiles.character_tile_stack_fixture',
	# 'fixtures.tiles.door_pattern_fixture',
	# 'fixtures.tiles.room_tile_fixture',
	# 'fixtures.tiles.room_tile_stack_fixture',
	# 'fixtures.tiles.tile_fixture',
	'fixtures.server.states.character_selection_state_fixture',
	'fixtures.server.states.lobby_state_fixture',
	'fixtures.server.core_fixture'
]

@pytest.fixture
def make_sprite():
	def _make_sprite(mocker, x=0, y=0, rotation=0.0, scale_x=1.0, scale_y=1.0):
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
def make_label():
	def _make_label(mocker, x=0, y=0):
		label = types.SimpleNamespace()
		label.draw = mocker.stub()
		label.x = x
		label.y = y
		return label
	return _make_label

@pytest.fixture
def make_connection():
	def _make_connection(mocker):
		connection = types.SimpleNamespace()
		connection.send = mocker.stub()
		return connection
	return _make_connection

@pytest.fixture
def make_node():
	def _make_node(mocker):
		node = types.SimpleNamespace()
		node.on_command = mocker.stub()
		node.on_update = mocker.stub()
		node.draw = mocker.stub()
		return node
	return _make_node

@pytest.fixture
def make_asset_manager():
	def _make_asset_manager(mocker):
		asset_manager = types.SimpleNamespace()
		asset_manager.common = {}
		for key, value in config.COMMON_ASSETS.items():
			if value['asset_type'] == 'single':
				asset_manager.common[key] = None
			else:
				asset_manager.common[key] = [None for i in range(value['rows'] * value['columns'])]
		asset_manager.characters = {}
		for character in config.CHARACTERS:
			asset_manager.characters[character['variable_name']] = None
		asset_manager.rooms = [None for i in range(config.ROOMS_ASSET['rows'] * config.ROOMS_ASSET['columns'])]
		return asset_manager
	return _make_asset_manager

@pytest.fixture
def get_args():
	def _get_args(stub, call_number, argument_number=None):
		if argument_number != None:
			return stub.call_args_list[call_number][0][argument_number]
		else:
			return stub.call_args_list[call_number][0]
	return _get_args

