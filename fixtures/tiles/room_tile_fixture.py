import pytest
from src.tiles import room_tile as room_tile_module, door_pattern as door_pattern_module

@pytest.fixture
def make_room_tile(make_sprite, make_label):
	def _make_room_tile(mocker, name='Room Tile Name', code=door_pattern_module.ONE_DOOR):
		mocker.patch('pyglet.sprite')
		mocker.patch('pyglet.text')
		room_tile = room_tile_module.RoomTile(name, { 'door': 'door', 'rooms': [0, 1, 2, 3], 'room_selected': 'room_selected'}, 0, code)
		room_tile.sprite = make_sprite(mocker)
		room_tile.selected = make_sprite(mocker)
		room_tile.label = make_label(mocker)
		room_tile.door_sprites[0] = make_sprite(mocker)
		room_tile.door_sprites[1] = make_sprite(mocker)
		room_tile.door_sprites[2] = make_sprite(mocker)
		room_tile.door_sprites[3] = make_sprite(mocker)
		return room_tile
	return _make_room_tile