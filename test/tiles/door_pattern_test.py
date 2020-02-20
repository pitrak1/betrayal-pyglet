import pytest
import pyglet
from src.tiles import door_pattern as door_pattern_module

@pytest.mark.usefixtures('make_door_patterns')
class TestDoorPattern():
	class TestConstructor():
		def test_creates_pattern_if_given_code(self):
			assert door_pattern_module.DoorPattern(door_pattern_module.ONE_DOOR) == [True, False, False, False]
			assert door_pattern_module.DoorPattern(door_pattern_module.RIGHT_ANGLE) == [True, True, False, False]
			assert door_pattern_module.DoorPattern(door_pattern_module.ACROSS) == [True, False, True, False]
			assert door_pattern_module.DoorPattern(door_pattern_module.ONE_WALL) == [True, True, True, False]
			assert door_pattern_module.DoorPattern(door_pattern_module.NO_WALLS) == [True, True, True, True]

		def test_creates_pattern_if_given_array(self):
			assert door_pattern_module.DoorPattern([False, False, True, False]).code == door_pattern_module.ONE_DOOR
			assert door_pattern_module.DoorPattern([False, True, True, False]).code == door_pattern_module.RIGHT_ANGLE
			assert door_pattern_module.DoorPattern([False, True, False, True]).code == door_pattern_module.ACROSS
			assert door_pattern_module.DoorPattern([True, False, True, True]).code == door_pattern_module.ONE_WALL
			assert door_pattern_module.DoorPattern([True, True, True, True]).code == door_pattern_module.NO_WALLS

	class TestRotate():
		def test_rotates_doors_to_front_of_array(self, make_door_patterns):
			pytest.one_door.rotate(3)
			assert pytest.one_door == [False, True, False, False]

	class TestGetRequiredDoorsInCommon():
		class TestWhenCodeIsOneDoor():
			def test_returns_1(self):
				assert pytest.one_door.get_required_doors_in_common([]) == 1

		class TestWhenCodeIsRightAngle():
			def test_returns_1_when_given_code_is_one_door_or_across(self):
				assert pytest.right_angle.get_required_doors_in_common(pytest.one_door) == 1
				assert pytest.right_angle.get_required_doors_in_common(pytest.across) == 1

			def test_returns_2_when_given_code_is_right_angle_one_wall_or_no_walls(self):
				assert pytest.right_angle.get_required_doors_in_common(pytest.right_angle) == 2
				assert pytest.right_angle.get_required_doors_in_common(pytest.one_wall) == 2
				assert pytest.right_angle.get_required_doors_in_common(pytest.no_walls) == 2

		class TestWhenCodeIsAcross():
			def test_returns_1_when_given_code_is_one_door_or_right_angle(self):
				assert pytest.across.get_required_doors_in_common(pytest.one_door) == 1
				assert pytest.across.get_required_doors_in_common(pytest.right_angle) == 1

			def test_returns_2_when_given_code_is_across_one_wall_or_no_walls(self):
				assert pytest.across.get_required_doors_in_common(pytest.across) == 2
				assert pytest.across.get_required_doors_in_common(pytest.one_wall) == 2
				assert pytest.across.get_required_doors_in_common(pytest.no_walls) == 2

		class TestWhenCodeOneWall():
			def test_returns_1_when_given_code_is_one_door(self):
				assert pytest.one_wall.get_required_doors_in_common(pytest.one_door) == 1

			def test_returns_2_when_given_code_is_right_angle_or_across(self):
				assert pytest.one_wall.get_required_doors_in_common(pytest.right_angle) == 2
				assert pytest.one_wall.get_required_doors_in_common(pytest.across) == 2

			def test_returns_3_when_given_code_is_one_wall_or_no_walls(self):
				assert pytest.one_wall.get_required_doors_in_common(pytest.one_wall) == 3
				assert pytest.one_wall.get_required_doors_in_common(pytest.no_walls) == 3

		class TestWhenCodeNoWalls():
			def test_returns_1_when_given_code_is_one_door(self):
				assert pytest.no_walls.get_required_doors_in_common(pytest.one_door) == 1

			def test_returns_2_when_given_code_is_right_angle_or_across(self):
				assert pytest.no_walls.get_required_doors_in_common(pytest.right_angle) == 2
				assert pytest.no_walls.get_required_doors_in_common(pytest.across) == 2

			def test_returns_3_when_given_code_is_one_wall(self):
				assert pytest.no_walls.get_required_doors_in_common(pytest.one_wall) == 3

			def test_returns_4_when_given_code_is_no_walls(self):
				assert pytest.no_walls.get_required_doors_in_common(pytest.no_walls) == 4

	class TestGetDoorsInCommon():
		def test_returns_the_number_of_doors_in_the_same_place(self):
			assert pytest.no_walls.get_doors_in_common(door_pattern_module.DoorPattern([True, False, True, True])) == 3
			assert pytest.across.get_doors_in_common(door_pattern_module.DoorPattern([True, False, True, False])) == 2
			assert pytest.across.get_doors_in_common(door_pattern_module.DoorPattern([False, True, False, True])) == 0

