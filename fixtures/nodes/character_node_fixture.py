import pytest
from src.nodes import character_node as character_node_module

@pytest.fixture
def make_character_node(make_character_tile):
	def _make_character_node(mocker, grid_position):
		return character_node_module.CharacterNode(make_character_tile(mocker), grid_position)
	return _make_character_node