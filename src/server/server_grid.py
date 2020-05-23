from lattice2d.grid import Actor, Tile, TileGrid, get_direction, reverse_direction
from src.common.grid import Room, RoomGrid
from src.common import constants
import config

class ServerRoomGrid(RoomGrid):
	def __init__(self):
		super().__init__()
		for room in config.STARTING_ROOMS:
			self.add_tile(room['grid_x'], room['grid_y'], Room(room))
