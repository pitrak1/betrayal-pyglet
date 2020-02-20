import pytest
from src.tiles import tile as tile_module

@pytest.fixture
def make_tile(make_sprite, make_label):
	def _make_tile(mocker, name='Tile Name'):
		mocker.patch('pyglet.sprite')
		mocker.patch('pyglet.text')
		tile = tile_module.Tile(name, 'image', 'image_selected')
		tile.sprite = make_sprite(mocker)
		tile.selected = make_sprite(mocker)
		tile.label = make_label(mocker)
		return tile
	return _make_tile