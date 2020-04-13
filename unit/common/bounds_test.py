from src.common import bounds as bounds_module

class TestBounds():
	class TestWithinCircleBounds():
		def test_returns_true_when_position_is_within_bounds(self, mocker):
			assert bounds_module.within_circle_bounds(0, 0, 19, 0, 20)
			assert bounds_module.within_circle_bounds(0, 0, 0, 19, 20)
			assert bounds_module.within_circle_bounds(0, 0, -13, -13, 20)

		def test_returns_false_when_position_is_outside_bounds(self, mocker):
			assert not bounds_module.within_circle_bounds(0, 0, 21, 0, 20)
			assert not bounds_module.within_circle_bounds(0, 0, 0, 21, 20)
			assert not bounds_module.within_circle_bounds(0, 0, -15, -15, 20)

	class TestWithinRectBounds():
		def test_returns_true_when_position_is_within_bounds(self, mocker):
			assert bounds_module.within_rect_bounds(0, 0, 19, 0, 40, 20)
			assert bounds_module.within_rect_bounds(0, 0, 0, 9, 40, 20)
			assert bounds_module.within_rect_bounds(0, 0, -19, -9, 40, 20)

		def test_returns_false_when_position_is_outside_bounds(self, mocker):
			assert not bounds_module.within_rect_bounds(0, 0, 21, 0, 40, 20)
			assert not bounds_module.within_rect_bounds(0, 0, 0, 11, 40, 20)
			assert not bounds_module.within_rect_bounds(0, 0, -21, -11, 40, 20)

	class TestWithinSquareBounds():
		def test_returns_true_when_position_is_within_bounds(self, mocker):
			assert bounds_module.within_square_bounds(0, 0, 19, 0, 40)
			assert bounds_module.within_square_bounds(0, 0, 0, 19, 40)
			assert bounds_module.within_square_bounds(0, 0, -19, -19, 40)

		def test_returns_false_when_position_is_outside_bounds(self, mocker):
			assert not bounds_module.within_square_bounds(0, 0, 21, 0, 40)
			assert not bounds_module.within_square_bounds(0, 0, 0, 21, 40)
			assert not bounds_module.within_square_bounds(0, 0, -21, -21, 40)
