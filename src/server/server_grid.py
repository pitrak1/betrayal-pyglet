from lattice2d.grid import TileGrid
from src.common.grid import Room, RoomGrid
from constants import Constants

class ServerRoomGrid(RoomGrid):
	def __init__(self, grid_dimensions):
		super().__init__(grid_dimensions)
		for room in Constants.starting_rooms:
			self.add_tile(room['grid_position'], Room(room))
