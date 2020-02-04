import pyglet
from src import assets
from src.world import room_node
from src.commands import add_room_command

MAP_WIDTH = 6
MAP_HEIGHT = 6

class World():
	def __init__(self):
		self.rooms = [[0] * MAP_WIDTH for i in range(MAP_HEIGHT)]
		self.characters = []
		
	def on_draw(self):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_draw()

	def on_command(self, command, command_queue):
		if isinstance(command, add_room_command.AddRoomCommand):
			self.__add_room(command)
		else:
			for room_row in self.rooms:
				for room in room_row:
					if isinstance(room, room_node.RoomNode):
						room.on_command(command, command_queue)

	def on_update(self, dt):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_update(dt)

	def __add_room(self, command):
		self.rooms[command.grid_x][command.grid_y] = room_node.RoomNode(command.img, command.img_highlighted, command.grid_x, command.grid_y)
