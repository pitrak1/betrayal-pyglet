import pyglet
from src.server import server_room_grid
from src.client.world.game import client_room
from src.shared import constants
import config

class ClientRoomGrid(server_room_grid.ServerRoomGrid):
	def __init__(self, testing=False):
		self.testing = testing
		super().__init__()

	def initialize_rooms(self):
		for room in config.STARTING_ROOMS:
			self.add_room(room['grid_x'], room['grid_y'], client_room.ClientRoom(room, self.testing))

	def add_player(self, grid_x, grid_y, player):
		if isinstance(self.rooms[grid_x][grid_y], client_room.ClientRoom):
			self.rooms[grid_x][grid_y].add_player(player)

	def default_handler(self, command, state=None):
		result = False
		for row in self.rooms:
			for room in row:
				if isinstance(room, client_room.ClientRoom):
					if room.on_command(command, state): result = True
		return result
