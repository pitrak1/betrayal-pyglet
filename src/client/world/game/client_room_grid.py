import pyglet
from src.server import server_room_grid as server_room_grid_module
from src.client.world.game import client_room as client_room_module
from src.shared import constants
import config

class ClientRoomGrid(server_room_grid_module.ServerRoomGrid):
	def __init__(self, asset_manager):
		self.asset_manager = asset_manager
		super().__init__()

	def initialize_rooms(self):
		for room in config.STARTING_ROOMS:
			self.add_room(room['grid_x'], room['grid_y'], client_room_module.ClientRoom(room, self.asset_manager))

	def add_player(self, grid_x, grid_y, player):
		self.rooms[grid_x][grid_y].players.append(player)
		player.portrait_sprite.update(x=grid_x * constants.GRID_SIZE, y=grid_y * constants.GRID_SIZE)
		player.selected_sprite.update(x=grid_x * constants.GRID_SIZE, y=grid_y * constants.GRID_SIZE)

	def client_translated_mouse_press_handler(self, command, state):
		if command.data['button'] == pyglet.window.mouse.LEFT:
			if not self.default_handler(command, state):
				state.select(None)

	def default_handler(self, command, state=None):
		result = False
		for row in self.rooms:
			for room in row:
				if isinstance(room, client_room_module.ClientRoom):
					if room.on_command(command, state): result = True
		return result

	def on_update(self, dt=None, state=None):
		for row in self.rooms:
			for room in row:
				if isinstance(room, client_room_module.ClientRoom):
					room.on_update(dt, state)

	def draw(self, state=None):
		for row in self.rooms:
			for room in row:
				if isinstance(room, client_room_module.ClientRoom):
					room.draw()