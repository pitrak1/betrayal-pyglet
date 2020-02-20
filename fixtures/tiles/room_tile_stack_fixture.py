import pytest
from src.tiles import room_tile_stack as room_tile_stack_module
from fixtures.tiles import room_tile_fixture

@pytest.fixture
def make_room_tile_stack(make_room_tile):
	def _make_room_tile_stack(mocker):
		mocker.patch('pyglet.sprite')
		mocker.patch('pyglet.text')
		room_tile_stack = room_tile_stack_module.RoomTileStack({ 
			'rooms': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ], 
			'room_selected': 'room_selected',
			'door': 'door'
		})
		room_tile_stack.stack.clear()
		room_tile_stack.stack.append(make_room_tile(mocker, 'Room Tile 1'))
		room_tile_stack.stack.append(make_room_tile(mocker, 'Room Tile 2'))
		room_tile_stack.stack.append(make_room_tile(mocker, 'Room Tile 3'))
		return room_tile_stack
	return _make_room_tile_stack