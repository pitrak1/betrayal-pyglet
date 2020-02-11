import pytest
import pyglet
from pyglet import sprite
from src.world import world_node
from src.commands import commands

class TestWorld():
	class TestOnDraw():
		def test_draws_rooms(self, mocker, make_world_node_with_stubbed_rooms):
			node = make_world_node_with_stubbed_rooms(mocker)
			node.on_draw()
			node.rooms[1][2].on_draw.assert_called_once()
			node.rooms[2][3].on_draw.assert_called_once()

	class TestOnCommand():
		class TestWithAddRoomCommand():
			def test_adds_room(self, mocker, make_world_node):
				node = make_world_node(mocker)
				command = commands.AddRoomCommand(img='img', img_selected='img', grid_x=1, grid_y=2)
				node.on_command(command, [command])
				assert node.rooms[1][2].__class__.__name__ == 'RoomNode'

			def test_does_not_pass_to_rooms(self, mocker, make_world_node_with_stubbed_rooms):
				node = make_world_node_with_stubbed_rooms(mocker)
				command = commands.AddRoomCommand(img='img', img_selected='img', grid_x=0, grid_y=0)
				node.on_command(command, [command])
				node.rooms[1][2].on_command.assert_not_called()
				node.rooms[2][3].on_command.assert_not_called()
		class TestWithOtherCommand():
			def test_passes_to_rooms(self, mocker, make_world_node_with_stubbed_rooms):
				node = make_world_node_with_stubbed_rooms(mocker)
				node.on_command('some command', ['some command'])
				node.rooms[1][2].on_command.assert_called_once_with('some command', ['some command'])
				node.rooms[2][3].on_command.assert_called_once_with('some command', ['some command'])

	class TestOnUpdate():
		def test_calls_on_update_for_rooms(self, mocker, make_world_node_with_stubbed_rooms):
			node = make_world_node_with_stubbed_rooms(mocker)
			node.on_update(1)
			node.rooms[1][2].on_update.assert_called_once_with(1)
			node.rooms[2][3].on_update.assert_called_once_with(1)
    