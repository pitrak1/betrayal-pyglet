import pyglet
from src.server import server_room_grid
from src.client.world.game import client_room
from src.shared import constants
import config

class ClientRoomGrid(server_room_grid.ServerRoomGrid):
	def _initialize_rooms(self):
		for room in config.STARTING_ROOMS:
			self._add_room(room['grid_x'], room['grid_y'], client_room.ClientRoom(room))

	def add_player(self, grid_x, grid_y, player):
		if isinstance(self._rooms[grid_x][grid_y], client_room.ClientRoom):
			print(f'confirmed {grid_x},{grid_y} is room')
			self._rooms[grid_x][grid_y].add_player(player)

	def default_handler(self, command, state=None):
		result = False
		for row in self._rooms:
			for room in row:
				if isinstance(room, client_room.ClientRoom):
					if room.on_command(command, state): result = True
		return result
