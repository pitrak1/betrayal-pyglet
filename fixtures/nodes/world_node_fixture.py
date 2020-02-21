import pytest
from src.nodes import world_node as world_node_module

@pytest.fixture
def make_world_node():
	def _make_world_node(mocker):
		world_node = world_node_module.WorldNode()
		mocker.patch.object(world_node, 'can_move', return_value=True)
		mocker.patch.object(world_node, 'is_room_rotation_valid', return_value=True)
		return world_node
	return _make_world_node