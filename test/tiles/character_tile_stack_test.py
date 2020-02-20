import pytest
import pyglet
from src.tiles import character_tile_stack as character_tile_stack_module

@pytest.mark.usefixtures("make_character_tile_stack")
class TestCharacterTileStack():
	class TestDraw():
		def test_pops_first_off_stack(self, mocker, make_character_tile_stack):
			character_tile_stack = make_character_tile_stack(mocker)
			tile = character_tile_stack.stack[0]
			assert character_tile_stack.draw() == tile

	class TestGetByName():
		def test_gets_character_tile_by_name(self, mocker, make_character_tile_stack):
			character_tile_stack = make_character_tile_stack(mocker)
			assert character_tile_stack.get_by_name('Character Tile 3').name == 'Character Tile 3'

		def test_raises_exception_if_tile_by_name_is_not_present(self, mocker, make_character_tile_stack):
			character_tile_stack = make_character_tile_stack(mocker)
			with pytest.raises(Exception) as exception:
				character_tile_stack.get_by_name('Character Tile 4')
			assert str(exception.value) == 'get_by_name failed because element by name was not in stack'
