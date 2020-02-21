import pyglet
from src import assets
from src.nodes import node, room_node, grid_node, room_grid
from src.tiles import room_tile, door_pattern
from src.utils import grid_position

class WorldNode(node.Node):
	def __init__(self):
		self.rooms = room_grid.RoomGrid(self)
		self.characters = []

	def is_room_rotation_valid(self, grid_pos, direction):
		room_doors = self.rooms.get_doors(grid_pos)
		existing_doors = door_pattern.DoorPattern([
			self.__has_door_in_direction(grid_pos.up(), grid_position.DOWN),
			self.__has_door_in_direction(grid_pos.right(), grid_position.LEFT),
			self.__has_door_in_direction(grid_pos.down(), grid_position.UP),
			self.__has_door_in_direction(grid_pos.left(), grid_position.RIGHT)
		])
		required_common_count = room_doors.get_required_doors_in_common(existing_doors)
		common_count = room_doors.get_doors_in_common(existing_doors)
		return required_common_count == common_count and room_doors[grid_position.reverse_direction(direction)]

	def __has_door_in_direction(self, grid_position, direction):
		try:
			return self.rooms.get_doors(grid_position)[direction]
		except:
			return False

	def can_move(self, start_grid_position, end_grid_position):
		try:
			direction = start_grid_position.grid_direction(end_grid_position)
		except Exception as e:
			return False

		if not self.rooms.is_room(end_grid_position): return True

		start_doors = self.rooms.get_doors(start_grid_position)
		end_doors = self.rooms.get_doors(end_grid_position)

		if direction == grid_position.UP:
			return start_doors[grid_position.UP] and end_doors[grid_position.DOWN]
		if direction == grid_position.RIGHT:
			return start_doors[grid_position.RIGHT] and end_doors[grid_position.LEFT]
		if direction == grid_position.DOWN:
			return start_doors[grid_position.DOWN] and end_doors[grid_position.UP]
		else:
			return start_doors[grid_position.LEFT] and end_doors[grid_position.RIGHT]
		
	def on_draw(self, state):
		self.rooms.on_draw(state)

	def add_room_handler(self, command, state):
		self.rooms.add_room(command)

	def default_handler(self, command, state):
		self.rooms.default_handler(lambda room : room.on_command(command, state))

	def on_update(self, dt, state):
		self.rooms.on_update(lambda room : room.on_update(dt, state))
