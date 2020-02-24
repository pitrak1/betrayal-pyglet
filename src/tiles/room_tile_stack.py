from src.tiles import room_tile as room_tile_module, tile_stack as tile_stack_module, door_pattern as door_pattern_module

class RoomTileStack(tile_stack_module.TileStack):
	def create_tiles(self, images, misc):
		selected = misc['room_selected']
		door = misc['door']
		self.stack.append(room_tile_module.RoomTile('Entrance Hall', images[0], selected, door, door_pattern_module.ONE_WALL))
		self.stack.append(room_tile_module.RoomTile('Foyer', images[1], selected, door, door_pattern_module.NO_WALLS))
		self.stack.append(room_tile_module.RoomTile('Grand Staircase', images[2], selected, door, door_pattern_module.ONE_DOOR))
		self.stack.append(room_tile_module.RoomTile('Dungeon', images[3], selected, door, door_pattern_module.ACROSS))
		self.stack.append(room_tile_module.RoomTile('Furnace Room', images[4], selected, door, door_pattern_module.ONE_WALL))
		self.stack.append(room_tile_module.RoomTile('Larder', images[5], selected, door, door_pattern_module.ACROSS))
		self.stack.append(room_tile_module.RoomTile('Pentagram Chamber', images[6], selected, door, door_pattern_module.ONE_DOOR))
		self.stack.append(room_tile_module.RoomTile('Stairs From Basement', images[7], selected, door, door_pattern_module.ACROSS))
		self.stack.append(room_tile_module.RoomTile('Stormy Cellar', images[8], selected, door, door_pattern_module.ONE_DOOR))
		self.stack.append(room_tile_module.RoomTile('Underground Lake', images[9], selected, door, door_pattern_module.RIGHT_ANGLE))

	def get_room_tile_handler(self, command, state):
		if command.name:
			state.set_room_tile(self.get_by_name(command.name))
		else:
			state.set_room_tile(self.draw())
