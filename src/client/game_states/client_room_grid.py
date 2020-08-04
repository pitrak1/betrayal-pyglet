import pyglet
from src.common.grid import RoomGrid
from src.client.game_states.client_empty_tile import ClientEmptyTile
from src.client.game_states.client_room import ClientRoom
from constants import STARTING_ROOMS

class ClientRoomGrid(RoomGrid):
	def __init__(self, add_command, grid_dimensions):
		super().__init__(grid_dimensions)
		self.children = []
		self.add_command = add_command
		for i in range(self.grid_dimensions[0] * self.grid_dimensions[1]):
			self.children.append(ClientEmptyTile(add_command, ((i % self.grid_dimensions[0]), (i // self.grid_dimensions[1])), self.base_position))
		for room in STARTING_ROOMS:
			self.add_tile(room['grid_position'], ClientRoom(room, add_command, base_position=self.base_position))
