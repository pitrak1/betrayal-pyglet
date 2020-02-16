from src.tiles import room_tile, tile_stack, door_pattern

class RoomTileStack(tile_stack.TileStack):
	def create_tiles(self, images):
		self.stack.append(room_tile.RoomTile('Entrance Hall', images, 0, door_pattern.ONE_WALL))
		self.stack.append(room_tile.RoomTile('Foyer', images, 1, door_pattern.NO_WALLS))
		self.stack.append(room_tile.RoomTile('Grand Staircase', images, 2, door_pattern.ONE_DOOR))
		self.stack.append(room_tile.RoomTile('Dungeon', images, 3, door_pattern.ACROSS))
		self.stack.append(room_tile.RoomTile('Furnace Room', images, 4, door_pattern.ONE_WALL))
		self.stack.append(room_tile.RoomTile('Larder', images, 5, door_pattern.ACROSS))
		self.stack.append(room_tile.RoomTile('Pentagram Chamber', images, 6, door_pattern.ONE_DOOR))
		self.stack.append(room_tile.RoomTile('Stairs From Basement', images, 7, door_pattern.ACROSS))
		self.stack.append(room_tile.RoomTile('Stormy Cellar', images, 8, door_pattern.ONE_DOOR))
		self.stack.append(room_tile.RoomTile('Underground Lake', images, 9, door_pattern.RIGHT_ANGLE))
