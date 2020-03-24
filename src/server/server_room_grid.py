from src.server import server_room
from src.shared import constants, node
import config

class ServerRoomGrid(node.Node):
	def __init__(self):
		super().__init__()
		self._rooms = []
		for i in range(constants.GRID_WIDTH):
			row = []
			for j in range(constants.GRID_HEIGHT):
				row.append(None)
			self._rooms.append(row)
		self._initialize_rooms()

	def _initialize_rooms(self):
		for room in config.STARTING_ROOMS:
			self._add_room(room['grid_x'], room['grid_y'], server_room.ServerRoom(room))

	def _add_room(self, grid_x, grid_y, room):
		self._rooms[grid_x][grid_y] = room
		room.set_position(grid_x, grid_y)

		print(f'adding room {room.display_name}')

		up_room = self._rooms[grid_x][grid_y + 1]
		if room.has_door(server_room.UP) and up_room and up_room.has_door(server_room.DOWN):
			print(f'adding link to {up_room.display_name}')
			room.add_link(up_room)
			up_room.add_link(room)

		right_room = self._rooms[grid_x + 1][grid_y]
		if room.has_door(server_room.RIGHT) and right_room and right_room.has_door(server_room.LEFT):
			print(f'adding link to {right_room.display_name}')
			room.add_link(right_room)
			right_room.add_link(room)

		down_room = self._rooms[grid_x][grid_y - 1]
		if room.has_door(server_room.DOWN) and down_room and down_room.has_door(server_room.UP):
			print(f'adding link to {down_room.display_name}')
			room.add_link(down_room)
			down_room.add_link(room)

		left_room = self._rooms[grid_x - 1][grid_y]
		if room.has_door(server_room.LEFT) and left_room and left_room.has_door(server_room.RIGHT):
			print(f'adding link to {left_room.display_name}')
			room.add_link(left_room)
			left_room.add_link(room)

	def add_player(self, grid_x, grid_y, player):
		if isinstance(self._rooms[grid_x][grid_y], server_room.ServerRoom):
			self._rooms[grid_x][grid_y].add_player(player)

	def can_move(self, start_x, start_y, end_x, end_y):
		start_room = self._rooms[start_x][start_y]
		end_room = self._rooms[end_x][end_y]
		print(f'attempting move from {start_room.display_name} to {end_room.display_name}')
		for link in start_room.links:
			print(link.display_name)
		return start_room and end_room and start_room.has_link(end_room)

	def move(self, player, start_x, start_y, end_x, end_y):
		start_room = self._rooms[start_x][start_y]
		end_room = self._rooms[end_x][end_y]
		start_room.remove_player(player)
		end_room.add_player(player)

