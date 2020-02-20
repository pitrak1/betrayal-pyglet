import pytest
import pyglet
from src.utils import position as position_module, grid_position as grid_position_module

@pytest.mark.usefixtures('make_room_tile')
class TestRoomTile():
	class TestSetPosition():
		def test_sets_room_positions_from_grid_position(self, mocker, make_room_tile):
			room_tile = make_room_tile(mocker)
			grid_position = grid_position_module.GridPosition(0, 0)
			mocker.patch.object(grid_position, 'get_door_position', return_value=position_module.Position(25, 35))
			room_tile.set_position(grid_position)
			room_tile.door_sprites[0].update.assert_called_once_with(x=25, y=35, rotation=0)
			room_tile.door_sprites[1].update.assert_called_once_with(x=25, y=35, rotation=90)
			room_tile.door_sprites[2].update.assert_called_once_with(x=25, y=35, rotation=180)
			room_tile.door_sprites[3].update.assert_called_once_with(x=25, y=35, rotation=270)

	class TestOnDraw():
		def test_draws_doors_if_present(self, mocker, make_room_tile):
			room_tile = make_room_tile(mocker, code=[True, False, False, True])
			room_tile.on_draw(True)
			room_tile.door_sprites[0].draw.assert_called_once()
			room_tile.door_sprites[1].draw.assert_not_called()
			room_tile.door_sprites[2].draw.assert_not_called()
			room_tile.door_sprites[3].draw.assert_called_once()

	class TestWithinBounds():
		def test_calls_within_square_bounds(self, mocker, make_room_tile):
			room_tile = make_room_tile(mocker)
			mocker.patch.object(room_tile.grid_position, 'within_square_bounds')
			room_tile.within_bounds('position')
			room_tile.grid_position.within_square_bounds.assert_called_once_with('position', grid_position_module.GRID_SIZE)
