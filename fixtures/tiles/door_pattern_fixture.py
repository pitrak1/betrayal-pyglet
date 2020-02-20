import pytest
from src.tiles import door_pattern as door_pattern_module

@pytest.fixture
def make_door_patterns():
	pytest.one_door = door_pattern_module.DoorPattern(door_pattern_module.ONE_DOOR)
	pytest.right_angle = door_pattern_module.DoorPattern(door_pattern_module.RIGHT_ANGLE)
	pytest.across = door_pattern_module.DoorPattern(door_pattern_module.ACROSS)
	pytest.one_wall = door_pattern_module.DoorPattern(door_pattern_module.ONE_WALL)
	pytest.no_walls = door_pattern_module.DoorPattern(door_pattern_module.NO_WALLS)