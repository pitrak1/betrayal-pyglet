import pyglet
from src.client.asset_manager import Assets
from src.common.grid import Room, RoomGrid
from src.common import constants
import config

class ClientRoom(Room):
	def __init__(self, entry):
		super().__init__(entry)
		self.base_x = constants.WINDOW_CENTER_X
		self.base_y = constants.WINDOW_CENTER_Y
		self.base_scale = 1.0

	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.room_sprite = pyglet.sprite.Sprite(
			Assets().rooms[self.asset_index],
			x=(self.grid_x * constants.GRID_SIZE * self.base_scale) + self.base_x,
			y=(self.grid_y * constants.GRID_SIZE * self.base_scale) + self.base_y,
			batch=renderer.get_batch(),
			group=renderer.get_group(1)
		)
		self.room_sprite.update(rotation=self.sprite_rotation * 90, scale=self.base_scale)
		self.other = [self.room_sprite]

	def client_adjust_grid_position_handler(self, command):
		self.base_x = command.data['base_x']
		self.base_y = command.data['base_y']

	def client_adjust_grid_scale_handler(self, command):
		self.base_scale = command.data['base_scale']

class ClientRoomGrid(RoomGrid):
	def __init__(self):
		super().__init__()
		self.base_x = constants.WINDOW_CENTER_X
		self.base_y = constants.WINDOW_CENTER_Y
		self.base_scale = 1.0
		for room in config.STARTING_ROOMS:
			self.add_tile(room['grid_x'], room['grid_y'], ClientRoom(room))

	def client_adjust_grid_position_handler(self, command):
		self.base_x += command.data['adjust_x']
		self.base_y += command.data['adjust_y']
		command.data.update({ 'base_x': self.base_x, 'base_y': self.base_y })
		self.default_handler(command)

	def client_adjust_grid_scale_handler(self, command):
		updated_scale = self.base_scale * command.data['adjust']
		if updated_scale >= 0.125 and updated_scale <= 1.0:
			self.base_scale = updated_scale
			command.data.update({ 'base_scale': self.base_scale })
			self.default_handler(command)
