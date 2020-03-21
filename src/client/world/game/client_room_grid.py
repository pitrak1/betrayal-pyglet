import pyglet
from src.server import server_room_grid
from src.client.world.game import client_room
from src.shared import constants
import config

class ClientRoomGrid(server_room_grid.ServerRoomGrid):
	def _initialize_rooms(self):
		for room in config.STARTING_ROOMS:
			self._add_room(room['grid_x'], room['grid_y'], client_room.ClientRoom(room))

	# def add_player(self, grid_x, grid_y, player):
	# 	self.rooms[grid_x][grid_y].players.append(player)
	# 	player.portrait_sprite.update(x=grid_x * constants.GRID_SIZE, y=grid_y * constants.GRID_SIZE)
	# 	player.selected_sprite.update(x=grid_x * constants.GRID_SIZE, y=grid_y * constants.GRID_SIZE)

	# def client_translated_mouse_press_handler(self, command, state):
	# 	if command.data['button'] == pyglet.window.mouse.LEFT:
	# 		if not self.default_handler(command, state):
	# 			state.select(None)

	def default_handler(self, command, state=None):
		result = False
		for row in self._rooms:
			for room in row:
				if isinstance(room, client_room.ClientRoom):
					if room.on_command(command, state): result = True
		return result

	# def on_update(self, dt=None, state=None):
	# 	for row in self.rooms:
	# 		for room in row:
	# 			if isinstance(room, client_room.ClientRoom):
	# 				room.on_update(dt, state)
