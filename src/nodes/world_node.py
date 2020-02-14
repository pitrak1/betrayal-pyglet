import pyglet
from src import assets
from src.nodes import node, room_node
from src.commands import commands

MAP_WIDTH = 6
MAP_HEIGHT = 6

class WorldNode(node.Node):
	def __init__(self, state_machine):
		super().__init__(state_machine)
		self.rooms = [[0] * MAP_WIDTH for i in range(MAP_HEIGHT)]
		self.characters = []
		
	def on_draw(self):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_draw()

	def add_room_handler(self, command):
		self.rooms[command.grid_x][command.grid_y] = room_node.RoomNode(self.state_machine, command.room_tile, command.grid_x, command.grid_y)

	def default_handler(self, command):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_command(command)

	def on_update(self, dt):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_update(dt)
