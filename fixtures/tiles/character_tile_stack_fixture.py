import pytest
from src.tiles import character_tile_stack as character_tile_stack_module
from fixtures.tiles import character_tile_fixture

@pytest.fixture
def make_character_tile_stack(make_character_tile):
	def _make_character_tile_stack(mocker):
		mocker.patch('pyglet.sprite')
		mocker.patch('pyglet.text')
		character_tile_stack = character_tile_stack_module.CharacterTileStack({ 'brandon_jaspers': 'brandon_jaspers', 'father_rhinehardt': 'father_rhinehardt', 'character_selected': 'character_selected' })
		character_tile_stack.stack.clear()
		character_tile_stack.stack.append(make_character_tile(mocker, 'Character Tile 1'))
		character_tile_stack.stack.append(make_character_tile(mocker, 'Character Tile 2'))
		character_tile_stack.stack.append(make_character_tile(mocker, 'Character Tile 3'))
		return character_tile_stack
	return _make_character_tile_stack