import pytest
import pyglet
import math
from src.utils import position as position_module

class TestPosition():
	class TestEquality():
		def test_is_equal_if_x_and_y_are_equal(self):
			position_1 = position_module.Position(1, 2)
			position_2 = position_module.Position(2, 3)
			position_2.set_position(1, 2)
			assert position_1 == position_2

	class TestWithinCircleBounds():
		def test_returns_true_if_within_circle_bounds(self):
			position = position_module.Position(0, 0)
			assert position.within_circle_bounds(position_module.Position(74, 0), 150)
			assert position.within_circle_bounds(position_module.Position(0, 49), 100)
			assert position.within_circle_bounds(position_module.Position(14 / math.sqrt(2), 14 / math.sqrt(2)), 30)

		def test_returns_false_if_not_within_circle_bounds(self):
			position = position_module.Position(0, 0)
			assert not position.within_circle_bounds(position_module.Position(76, 0), 150)
			assert not position.within_circle_bounds(position_module.Position(0, 51), 100)
			assert not position.within_circle_bounds(position_module.Position(16 / math.sqrt(2), 16 / math.sqrt(2)), 30)

	class TestWithinSquareBounds():
		def test_returns_true_if_within_square_bounds(self):
			position = position_module.Position(0, 0)
			assert position.within_square_bounds(position_module.Position(74, 0), 150)
			assert position.within_square_bounds(position_module.Position(0, 49), 100)
			assert position.within_square_bounds(position_module.Position(14, 14), 30)

		def test_returns_false_if_not_within_square_bounds(self):
			position = position_module.Position(0, 0)
			assert not position.within_square_bounds(position_module.Position(76, 0), 150)
			assert not position.within_square_bounds(position_module.Position(0, 51), 100)
			assert not position.within_square_bounds(position_module.Position(16, 16), 30)
    