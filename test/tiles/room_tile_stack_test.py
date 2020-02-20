import pytest
import pyglet
from src.tiles import room_tile_stack as room_tile_stack_module

@pytest.mark.usefixtures("make_room_tile_stack")
class TestRoomTileStack():
	class TestDraw():
		def test_pops_first_off_stack(self, mocker, make_room_tile_stack):
			room_tile_stack = make_room_tile_stack(mocker)
			tile = room_tile_stack.stack[0]
			assert room_tile_stack.draw() == tile

	class TestGetByName():
		def test_gets_room_tile_by_name(self, mocker, make_room_tile_stack):
			room_tile_stack = make_room_tile_stack(mocker)
			assert room_tile_stack.get_by_name('Room Tile 3').name == 'Room Tile 3'

		def test_raises_exception_if_tile_by_name_is_not_present(self, mocker, make_room_tile_stack):
			room_tile_stack = make_room_tile_stack(mocker)
			with pytest.raises(Exception) as exception:
				room_tile_stack.get_by_name('Room Tile 4')
			assert str(exception.value) == 'get_by_name failed because element by name was not in stack'
