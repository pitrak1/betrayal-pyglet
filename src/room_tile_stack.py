from src import room_tile
import random

class RoomTileStack():
	def __init__(self, images):
		self.images = images
		self.stack = []
		self.__create_room_tiles()
		random.shuffle(self.stack)

	def __create_room_tiles(self):
		self.stack.append(room_tile.RoomTile(self.images, 'Dungeon', 0, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile(self.images, 'Furnace Room', 1, room_tile.PATTERN_ONE_WALL))
		self.stack.append(room_tile.RoomTile(self.images, 'Larder', 2, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile(self.images, 'Pentagram Chamber', 3, room_tile.PATTERN_ONE_DOOR))
		self.stack.append(room_tile.RoomTile(self.images, 'Stairs From Basement', 4, room_tile.PATTERN_ACROSS))
		self.stack.append(room_tile.RoomTile(self.images, 'Stormy Cellar', 5, room_tile.PATTERN_ONE_DOOR))
		self.stack.append(room_tile.RoomTile(self.images, 'Underground Lake', 6, room_tile.PATTERN_RIGHT_ANGLE))

	def draw(self):
		return self.stack.pop(0)