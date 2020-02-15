import pyglet
from src import assets
from src.nodes import node, room_node, grid_node
from src.commands import commands
from src.tiles import room_tile

MAP_WIDTH = 20
MAP_HEIGHT = 20

class WorldNode(node.Node):
	def __init__(self, state_machine):
		super().__init__(state_machine)
		self.rooms = []
		for i in range(MAP_WIDTH):
			room_row = []
			for j in range(MAP_HEIGHT):
				room_row.append(grid_node.GridNode(state_machine, i, j, self))
			self.rooms.append(room_row)
		self.characters = []

	def is_valid(self, grid_x, grid_y, direction):
		room_doors = self.rooms[grid_x][grid_y].tile.door_presence
		room_pattern = self.rooms[grid_x][grid_y].tile.pattern

		existing_doors = [
			self.rooms[grid_x][grid_y + 1].tile.door_presence[2] if isinstance(self.rooms[grid_x][grid_y + 1], room_node.RoomNode) else False,
			self.rooms[grid_x + 1][grid_y].tile.door_presence[3] if isinstance(self.rooms[grid_x + 1][grid_y], room_node.RoomNode) else False,
			self.rooms[grid_x][grid_y - 1].tile.door_presence[0] if isinstance(self.rooms[grid_x][grid_y - 1], room_node.RoomNode) else False,
			self.rooms[grid_x - 1][grid_y].tile.door_presence[1] if isinstance(self.rooms[grid_x - 1][grid_y], room_node.RoomNode) else False
		]
		existing_doors_pattern = room_tile.find_pattern(existing_doors)
		existing_doors_count = existing_doors.count(True)

		if room_pattern == 0:
			required = 1
		elif room_pattern == 1:
			if existing_doors_pattern == 0:
				required = 1
			elif existing_doors_pattern == 1:
				required = 2
			elif existing_doors_pattern == 2:
				required = 1
			else:
				required = 2
		elif room_pattern == 2:
			if existing_doors_pattern == 0:
				required = 1
			elif existing_doors_pattern == 1:
				required = 1
			elif existing_doors_pattern == 2:
				required = 2
			else:
				required = 2
		elif room_pattern == 3:
			required = min([3, existing_doors_count])
		elif room_pattern == 4:
			required = min([3, existing_doors_count])

		common_count = 0
		for i in range(4):
			if room_doors[i] and room_doors[i] == existing_doors[i]: common_count = common_count + 1

		return common_count == required and room_doors[(direction + 2) % 4]

	def __doors_in_common(self, doors1, doors2):
		count = 0
		for i in range(4):
			if doors1[i] and doors1[i] == doors2[i]: count = count + 1
		return count

	def can_move(self, start_x, start_y, end_x, end_y):
		direction = self.move_direction(start_x, start_y, end_x, end_y)
		start_doors = self.rooms[start_x][start_y].tile.door_presence
		end_doors = self.rooms[end_x][end_y].tile.door_presence if isinstance(self.rooms[end_x][end_y], room_node.RoomNode) else []

		if direction == 0:
			return start_doors[0] and not (end_doors and not end_doors[2])
		if direction == 1:
			return start_doors[1] and not (end_doors and not end_doors[3])
		if direction == 2:
			return start_doors[2] and not (end_doors and not end_doors[0])
		if direction == 3:
			return start_doors[3] and not (end_doors and not end_doors[1])
		else:
			return False

	def move_direction(self, start_x, start_y, end_x, end_y):
		if abs(start_x - end_x) + abs(start_y - end_y) > 1: return -1

		if start_x == end_x:
			return 2 if start_y > end_y else 0
		else:
			return 3 if start_x > end_x else 1
		
	def on_draw(self):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_draw()

	def add_room_handler(self, command):
		self.rooms[command.grid_x][command.grid_y] = room_node.RoomNode(self.state_machine, command.room_tile, command.grid_x, command.grid_y, self)
		self.rooms[command.grid_x][command.grid_y].tile.rotate(command.rotation)

	def default_handler(self, command):
		for room_row in self.rooms:
			for room in room_row:
				room.on_command(command)

	def on_update(self, dt):
		for room_row in self.rooms:
			for room in room_row:
				if isinstance(room, room_node.RoomNode):
					room.on_update(dt)
