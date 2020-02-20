import pytest
import pyglet
from src.utils import grid_position as grid_position_module, position as position_module

class TestReverseDirection():
	def test_returns_direction_opposite_to_given(self):
		assert grid_position_module.reverse_direction(grid_position_module.DOWN) == grid_position_module.UP
		assert grid_position_module.reverse_direction(grid_position_module.RIGHT) == grid_position_module.LEFT

class TestGridPosition():
	class TestEquality():
		def test_is_equal_if_grid_x_and_grid_y_are_equal(self):
			grid_position_1 = grid_position_module.GridPosition(1, 2)
			grid_position_2 = grid_position_module.GridPosition(2, 3)
			grid_position_2.set_grid_position(1, 2)
			assert grid_position_1 == grid_position_2

	class TestGridDistance():
		def test_returns_distance_from_point_based_on_grid(self):
			grid_position_1 = grid_position_module.GridPosition(0, 0)
			grid_position_2 = grid_position_module.GridPosition(2, 3)
			assert grid_position_1.grid_distance(grid_position_2) == 5

	class TestGridDirection():
		def test_raises_exception_if_distance_is_greater_than_1(self):
			grid_position_1 = grid_position_module.GridPosition(0, 0)
			grid_position_2 = grid_position_module.GridPosition(2, 3)
			with pytest.raises(Exception) as exception:
				grid_position_1.grid_direction(grid_position_2)
			assert str(exception.value) == 'direction cannot be computed for distances greater than 1'

		def test_raises_exception_if_distance_is_zero(self):
			grid_position_1 = grid_position_module.GridPosition(0, 0)
			grid_position_2 = grid_position_module.GridPosition(0, 0)
			with pytest.raises(Exception) as exception:
				grid_position_1.grid_direction(grid_position_2)
			assert str(exception.value) == 'direction cannot be computed to self'

		def test_returns_direction_from_start_to_end(self):
			grid_position = grid_position_module.GridPosition(0, 0)
			grid_position_right = grid_position_module.GridPosition(1, 0)
			grid_position_down = grid_position_module.GridPosition(0, -1)
			assert grid_position.grid_direction(grid_position_right) == grid_position_module.RIGHT
			assert grid_position.grid_direction(grid_position_down) == grid_position_module.DOWN

	class TestGetDoorPosition():
		def test_returns_position_for_door_in_given_direction(self):
			grid_position = grid_position_module.GridPosition(0, 0)
			offset = grid_position_module.GRID_SIZE // 2 - grid_position_module.DOOR_OFFSET
			assert grid_position.get_door_position(grid_position_module.UP) == position_module.Position(0, offset)
			assert grid_position.get_door_position(grid_position_module.RIGHT) == position_module.Position(offset, 0)
			assert grid_position.get_door_position(grid_position_module.DOWN) == position_module.Position(0, -offset)
			assert grid_position.get_door_position(grid_position_module.LEFT) == position_module.Position(-offset, 0)

	class TestUp():
		def test_returns_grid_position_for_one_grid_position_up(self):
			grid_position = grid_position_module.GridPosition(0, 0)
			assert grid_position.up() == grid_position_module.GridPosition(0, 1)

	class TestRight():
		def test_returns_grid_position_for_one_grid_position_right(self):
			grid_position = grid_position_module.GridPosition(0, 0)
			assert grid_position.right() == grid_position_module.GridPosition(1, 0)

	class TestDown():
		def test_returns_grid_position_for_one_grid_position_down(self):
			grid_position = grid_position_module.GridPosition(0, 0)
			assert grid_position.down() == grid_position_module.GridPosition(0, -1)

	class TestLeft():
		def test_returns_grid_position_for_one_grid_position_left(self):
			grid_position = grid_position_module.GridPosition(0, 0)
			assert grid_position.left() == grid_position_module.GridPosition(-1, 0)

	class TestCopy():
		def test_returns_grid_position_for_one_grid_position_left(self):
			grid_position = grid_position_module.GridPosition(0, 0)
			grid_position_copy = grid_position.copy()
			grid_position.set_grid_position(9, 9)
			assert grid_position_copy == grid_position_module.GridPosition(0, 0)