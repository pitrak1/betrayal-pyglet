import pytest
import pyglet
from src.tiles import character_tile as character_tile_module

@pytest.mark.usefixtures('make_character_tile')
class TestCharacterTile():
	class TestWithinBounds():
		def test_calls_within_circle_bounds(self, mocker, make_character_tile):
			character_tile = make_character_tile(mocker)
			mocker.patch.object(character_tile.grid_position, 'within_circle_bounds')
			character_tile.within_bounds('position')
			character_tile.grid_position.within_circle_bounds.assert_called_once_with('position', character_tile_module.CHARACTER_SIZE)
    