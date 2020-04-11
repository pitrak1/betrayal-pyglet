from src.server import server_room
from src.common import constants, node
import config

class ServerRoomGrid(node.Node):
	def __init__(self):
		super().__init__()
		self.rooms = []
		for i in range(constants.GRID_WIDTH):
			row = []
			for j in range(constants.GRID_HEIGHT):
				row.append(None)
			self.rooms.append(row)
		self.initialize_rooms()

	def initialize_rooms(self):
		for room in config.STARTING_ROOMS:
			self.add_room(room['grid_x'], room['grid_y'], server_room.ServerRoom(room))

	def add_room(self, grid_x, grid_y, room):
		self.rooms[grid_x][grid_y] = room
		room.set_position(grid_x, grid_y)

		up_room = self.rooms[grid_x][grid_y + 1]
		if room.has_door(server_room.UP) and up_room and up_room.has_door(server_room.DOWN):
			room.add_link(up_room)
			up_room.add_link(room)

		right_room = self.rooms[grid_x + 1][grid_y]
		if room.has_door(server_room.RIGHT) and right_room and right_room.has_door(server_room.LEFT):
			room.add_link(right_room)
			right_room.add_link(room)

		down_room = self.rooms[grid_x][grid_y - 1]
		if room.has_door(server_room.DOWN) and down_room and down_room.has_door(server_room.UP):
			room.add_link(down_room)
			down_room.add_link(room)

		left_room = self.rooms[grid_x - 1][grid_y]
		if room.has_door(server_room.LEFT) and left_room and left_room.has_door(server_room.RIGHT):
			room.add_link(left_room)
			left_room.add_link(room)

	def add_player(self, grid_x, grid_y, player):
		if isinstance(self.rooms[grid_x][grid_y], server_room.ServerRoom):
			self.rooms[grid_x][grid_y].add_player(player)

	# def can_move(self, start_x, start_y, end_x, end_y):
	# 	start_room = self.rooms[start_x][start_y]
	# 	end_room = self.rooms[end_x][end_y]
	# 	return start_room and end_room and start_room.has_link(end_room)

	# def move(self, player, start_x, start_y, end_x, end_y):
	# 	start_room = self.rooms[start_x][start_y]
	# 	end_room = self.rooms[end_x][end_y]
	# 	start_room.remove_player(player)
	# 	end_room.add_player(player)

