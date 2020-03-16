from src.server import server_room as server_room_module
from src.shared import constants, node as node_module
import config

class ServerRoomGrid(node_module.Node):
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
			self.add_room(room['grid_x'], room['grid_y'], server_room_module.ServerRoom(room))

	def add_room(self, grid_x, grid_y, room):
		self.rooms[grid_x][grid_y] = room
		room.set_position(grid_x, grid_y)

		up_room = self.rooms[grid_x][grid_y + 1]
		if room.doors[server_room_module.UP] and up_room and up_room.doors[server_room_module.DOWN]:
			room.links.append(up_room)
			up_room.links.append(room)

		right_room = self.rooms[grid_x + 1][grid_y]
		if room.doors[server_room_module.RIGHT] and right_room and right_room.doors[server_room_module.LEFT]:
			room.links.append(right_room)
			right_room.links.append(room)

		down_room = self.rooms[grid_x][grid_y - 1]
		if room.doors[server_room_module.DOWN] and down_room and down_room.doors[server_room_module.UP]:
			room.links.append(down_room)
			down_room.links.append(room)

		left_room = self.rooms[grid_x - 1][grid_y]
		if room.doors[server_room_module.LEFT] and left_room and left_room.doors[server_room_module.RIGHT]:
			room.links.append(left_room)
			left_room.links.append(room)

		print(f'putting {room.display_name} at {grid_x}, {grid_y}')
		print_links = ''
		for link in room.links:
			print_links += f'{link.display_name}, '
		print(f'links: {print_links[:-2]}')

	def add_player(self, grid_x, grid_y, player):
		self.rooms[grid_x][grid_y].players.append(player)

	def can_move(self, start_x, start_y, end_x, end_y):
		start_room = self.rooms[start_x][start_y]
		end_room = self.rooms[end_x][end_y]
		return start_room and end_room and end_room in start_room.links

