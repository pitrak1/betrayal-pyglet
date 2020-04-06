import pytest
import pyglet
from src.server import server_player, server_room, server_room_grid
from src.shared import command
import types

class TestServerRoomGrid():
	class TestAddRoom():
		def create_room(self, mocker, has_door_direction):
			room = types.SimpleNamespace()
			room.set_position = mocker.stub()
			room.has_door = lambda direction : direction == has_door_direction
			room.add_link = mocker.stub()
			return room

		def test_sets_position_on_room(self, mocker):
			room = self.create_room(mocker, None)
			room_grid = server_room_grid.ServerRoomGrid()
			room_grid.add_room(1, 2, room)
			room.set_position.assert_called_once_with(1, 2)

		def test_does_not_add_links_if_room_does_not_have_door(self, mocker):
			room = self.create_room(mocker, None)
			up_room = self.create_room(mocker, server_room.DOWN)
			room_grid = server_room_grid.ServerRoomGrid()
			room_grid.rooms[1][3] = up_room
			room_grid.add_room(1, 2, room)
			room.add_link.assert_not_called()

		def test_does_not_add_links_if_other_room_does_not_exit(self, mocker):
			room = self.create_room(mocker, server_room.UP)
			room_grid = server_room_grid.ServerRoomGrid()
			room_grid.add_room(1, 2, room)
			room.add_link.assert_not_called()

		def test_does_not_add_links_if_other_room_does_not_have_door(self, mocker):
			room = self.create_room(mocker, server_room.UP)
			up_room = self.create_room(mocker, None)
			room_grid = server_room_grid.ServerRoomGrid()
			room_grid.rooms[1][3] = up_room
			room_grid.add_room(1, 2, room)
			room.add_link.assert_not_called()

		def test_adds_links_if_other_room_exists_and_doors_align(self, mocker):
			room = self.create_room(mocker, server_room.UP)
			up_room = self.create_room(mocker, server_room.DOWN)
			room_grid = server_room_grid.ServerRoomGrid()
			room_grid.rooms[1][3] = up_room
			room_grid.add_room(1, 2, room)
			room.add_link.assert_called_once_with(up_room)
			up_room.add_link.assert_called_once_with(room)
