import pytest
import pyglet
from src.server.server_grid import ServerRoomGrid
from lattice2d.grid import UP, RIGHT, DOWN, LEFT, Tile
import types

class TestServerGrid():
	class TestServerRoomGrid():
		class TestAddAdjacentLinks():
			class TestTile(Tile):
				def __init__(self, grid_position, doors):
					super().__init__(grid_position)
					self.doors = doors
					self.links = []

			def test_adds_links_if_aligned_doors(self):
				grid = ServerRoomGrid()
				start_tile = self.TestTile((0, 0), [True, False, False, False])
				end_tile = self.TestTile((0, 1), [False, False, True, False])
				grid.add_adjacent_links(start_tile, end_tile)
				assert start_tile.links == [end_tile]
				assert end_tile.links == [start_tile]

			def test_does_not_add_links_if_doors_not_aligned(self):
				grid = ServerRoomGrid()
				start_tile = self.TestTile((0, 0), [False, True, False, False])
				end_tile = self.TestTile((1, 0), [True, False, False, False])
				grid.add_adjacent_links(start_tile, end_tile)
				assert len(start_tile.links) == 0
				assert len(end_tile.links) == 0
