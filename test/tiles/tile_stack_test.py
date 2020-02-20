import pytest
import pyglet
from src.tiles import tile_stack as tile_stack_module

class TestTileStack():
	class TestConstructor():
		def test_constructor_raises_exception(self):
			with pytest.raises(NotImplementedError) as exception:
				tile_stack_module.TileStack('images')
			assert str(exception.value) == 'create_tiles must be overridden'
