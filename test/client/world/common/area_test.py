import pytest
import pyglet
from src.client.world.common import area as area_module

class TestArea():
	class TestWithinBounds():
		def test_returns_true_when_position_is_within_bounds(self, mocker):
			mocker.patch('pyglet.sprite')
			area = area_module.Area(range(9), 0, 0, 3, 5)
			assert area.within_bounds(1.5 * area_module.ASSET_TILE_SIZE - 1, 0)
			assert area.within_bounds(0, 2.5 * area_module.ASSET_TILE_SIZE - 1)
			assert area.within_bounds(-1.5 * area_module.ASSET_TILE_SIZE + 1, -2.5 * area_module.ASSET_TILE_SIZE + 1)

		def test_returns_false_when_position_is_outside_bounds(self, mocker):
			mocker.patch('pyglet.sprite')
			area = area_module.Area(range(9), 0, 0, 3, 5)
			assert not area.within_bounds(1.5 * area_module.ASSET_TILE_SIZE + 1, 0)
			assert not area.within_bounds(0, 2.5 * area_module.ASSET_TILE_SIZE + 1)
			assert not area.within_bounds(-1.5 * area_module.ASSET_TILE_SIZE - 1, -2.5 * area_module.ASSET_TILE_SIZE - 1)
