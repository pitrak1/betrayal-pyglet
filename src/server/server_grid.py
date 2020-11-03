from lattice2d.grid import TileGrid
from src.common.grid import Room, RoomGrid
from constants import STARTING_ROOMS

class ServerRoomGrid(RoomGrid):
	def __init__(self, grid_dimensions):
		super().__init__(grid_dimensions)
		for room in STARTING_ROOMS:
			self.add_tile(room['grid_position'], Room(room))
