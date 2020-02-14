from src.tiles import room_tile, tile_stack

class RoomTileStack(tile_stack.TileStack):
	def create_tiles(self, images):
		self.stack.append(room_tile.RoomTile('Dungeon', images, 0, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile('Furnace Room', images, 1, room_tile.PATTERN_ONE_WALL))
		self.stack.append(room_tile.RoomTile('Larder', images, 2, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile('Pentagram Chamber', images, 3, room_tile.PATTERN_ONE_DOOR))
		self.stack.append(room_tile.RoomTile('Stairs From Basement', images, 4, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile('Stormy Cellar', images, 5, room_tile.PATTERN_ONE_DOOR))
		self.stack.append(room_tile.RoomTile('Underground Lake', images, 6, room_tile.PATTERN_RIGHT_ANGLE))
