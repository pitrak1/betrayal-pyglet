from src.tiles import room_tile, tile_stack

class RoomTileStack(tile_stack.TileStack):
	def create_tiles(self, images):
		self.stack.append(room_tile.RoomTile('Entrance Hall', images, 0, room_tile.PATTERN_ONE_WALL))
		self.stack.append(room_tile.RoomTile('Foyer', images, 1, room_tile.PATTERN_NO_WALLS))
		self.stack.append(room_tile.RoomTile('Grand Staircase', images, 2, room_tile.PATTERN_ONE_DOOR))
		self.stack.append(room_tile.RoomTile('Dungeon', images, 3, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile('Furnace Room', images, 4, room_tile.PATTERN_ONE_WALL))
		self.stack.append(room_tile.RoomTile('Larder', images, 5, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile('Pentagram Chamber', images, 6, room_tile.PATTERN_ONE_DOOR))
		self.stack.append(room_tile.RoomTile('Stairs From Basement', images, 7, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile('Stormy Cellar', images, 8, room_tile.PATTERN_ONE_DOOR))
		self.stack.append(room_tile.RoomTile('Underground Lake', images, 9, room_tile.PATTERN_RIGHT_ANGLE))
