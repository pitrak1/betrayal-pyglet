from src import node as node_module
from src.world import empty_space as empty_space_module, room as room_module
from src.utils import constants, grid as grid_module
from src.tiles import door_pattern as door_pattern_module

class RoomGrid(node_module.Node):
	def __init__(self):
		self.rooms = []
		for i in range(constants.GRID_WIDTH):
			row = []
			for j in range(constants.GRID_HEIGHT):
				row.append(empty_space_module.EmptySpace(i, j))
			self.rooms.append(row)

	def on_draw(self, state):
		for row in self.rooms:
			for room in row:
				if isinstance(room, room_module.Room):
					room.on_draw(state)

	def place_room_handler(self, command, state):
		self.rooms[command.grid_x][command.grid_y] = room_module.Room(command.room_tile, command.grid_x, command.grid_y)
		self.rooms[command.grid_x][command.grid_y].tile.doors.rotate(command.rotation)

	def get_selected_character_move_valid_handler(self, command, state):
		try:
			direction = grid_module.get_direction(command.start_x, command.start_y, command.end_x, command.end_y)
		except Exception as e:
			state.set_selected_character_move_valid(False)
			return

		if not isinstance(self.rooms[command.end_x][command.end_y], room_module.Room): 
			state.set_selected_character_move_valid(True)
			return

		start_doors = self.rooms[command.start_x][command.start_y].tile.doors
		end_doors = self.rooms[command.end_x][command.end_y].tile.doors

		if direction == constants.UP:
			state.set_selected_character_move_valid(start_doors[constants.UP] and end_doors[constants.DOWN])
		elif direction == constants.RIGHT:
			state.set_selected_character_move_valid(start_doors[constants.RIGHT] and end_doors[constants.LEFT])
		elif direction == constants.DOWN:
			state.set_selected_character_move_valid(start_doors[constants.DOWN] and end_doors[constants.UP])
		else:
			state.set_selected_character_move_valid(start_doors[constants.LEFT] and end_doors[constants.RIGHT])

	def get_room_rotation_valid_handler(self, command, state):
		room_doors = self.rooms[command.grid_x][command.grid_y].tile.doors
		existing_doors = door_pattern_module.DoorPattern([
			self.__has_door_in_direction(command.grid_x, command.grid_y + 1, constants.DOWN),
			self.__has_door_in_direction(command.grid_x + 1, command.grid_y, constants.LEFT),
			self.__has_door_in_direction(command.grid_x, command.grid_y - 1, constants.UP),
			self.__has_door_in_direction(command.grid_x - 1, command.grid_y, constants.RIGHT)
		])
		required_common_count = room_doors.get_required_doors_in_common(existing_doors)
		common_count = room_doors.get_doors_in_common(existing_doors)
		state.set_room_rotation_valid(required_common_count == common_count and room_doors[(command.entering_direction + 2) % 4])

	def __has_door_in_direction(self, grid_x, grid_y, direction):
		if isinstance(self.rooms[grid_x][grid_y], room_module.Room):
			return self.rooms[grid_x][grid_y].tile.doors[direction]
		else:
			return False

	def default_handler(self, command, state):
		for row in self.rooms:
			for room in row:
				room.on_command(command, state)

	def on_update(self, dt, state):
		for row in self.rooms:
			for room in row:
				if isinstance(room, room_module.Room):
					room.on_update(dt, state)
