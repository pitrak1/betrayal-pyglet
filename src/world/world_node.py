import pyglet
from src import assets
from src.world import room_node
from src.commands import commands

MAP_WIDTH = 6
MAP_HEIGHT = 6

class WorldNode():
	def __init__(self, state_machine):
		self.state_machine = state_machine
		self.rooms = [[0] * MAP_WIDTH for i in range(MAP_HEIGHT)]
		self.characters = []
		
	def on_draw(self):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_draw()

	def on_command(self, command):
		if isinstance(command, commands.AddRoomCommand):
			self.__add_room(command)
		else:
			for room_row in self.rooms:
				for room in room_row:
					if isinstance(room, room_node.RoomNode):
						room.on_command(command)

	def on_update(self, dt):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_update(dt)

	def __add_room(self, command):
		self.rooms[command.grid_x][command.grid_y] = room_node.RoomNode(command.room_tile, command.grid_x, command.grid_y, self.state_machine)
