from lattice2d.grid.tile_grid import TileGrid
from lattice2d.grid.tile import Tile
from constants import STARTING_ROOMS

class ServerRoomGrid(TileGrid):
	def __init__(self):
		super().__init__()
		for room in STARTING_ROOMS:
			self.add_tile(room['grid_position'], Room(room))
