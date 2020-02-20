import pytest
from src.tiles import character_tile as character_tile_module

@pytest.fixture
def make_character_tile(make_sprite, make_label):
	def _make_character_tile(mocker, name='Character Tile Name'):
		mocker.patch('pyglet.sprite')
		mocker.patch('pyglet.text')
		character_tile = character_tile_module.CharacterTile(name, { 'asset': 'asset', 'character_selected': 'character_selected'}, 'asset')
		character_tile.sprite = make_sprite(mocker)
		character_tile.selected = make_sprite(mocker)
		character_tile.label = make_label(mocker)
		return character_tile
	return _make_character_tile