import pyglet
import sys
from lattice2d.full.full_client import FullClientState, Renderer
from lattice2d.full.full_server import FullServerPlayerList
from lattice2d.utilities.pagination import get_page_info
from lattice2d.network import NetworkCommand
from lattice2d.nodes import Node, Command
from lattice2d.grid import Actor, EmptyTile, Tile, TileGrid, get_direction, reverse_direction
from src.client.client_components import Background, Area, Button, TextBox
from src.common import constants
from src.client.asset_manager import Assets
from src.server.server_grid import ServerRoomGrid, ServerRoom, ServerPlayer
import config

class ClientRoom(ServerRoom):
	def __init__(self, entry):
		super().__init__(entry)
		self.base_x = 0
		self.base_y = 0

	def redraw_handler(self, command):
		renderer = command.data['renderer']
		self.room_sprite = pyglet.sprite.Sprite(
			Assets().rooms[self.asset_index],
			x=self.grid_x * constants.GRID_SIZE + self.base_x,
			y=self.grid_y * constants.GRID_SIZE + self.base_y,
			batch=renderer.get_batch(),
			group=renderer.get_group(1)
		)
		self.room_sprite.update(rotation=self.sprite_rotation * 90)
		self.other = [self.room_sprite]

	def client_adjust_grid_handler(self, command):
		self.base_x = command.data['base_x']
		self.base_y = command.data['base_y']

class ClientRoomGrid(TileGrid):
	def __init__(self):
		super().__init__(constants.GRID_WIDTH, constants.GRID_HEIGHT)
		self.base_x = 0
		self.base_y = 0
		for room in config.STARTING_ROOMS:
			self.add_tile(room['grid_x'], room['grid_y'], ClientRoom(room))

	def add_adjacent_links(self, start_tile, end_tile):
		if isinstance(end_tile, EmptyTile): return
		direction = get_direction(start_tile.grid_x, start_tile.grid_y, end_tile.grid_x, end_tile.grid_y)
		if start_tile.doors[direction] and end_tile.doors[reverse_direction(direction)]:
			start_tile.links.append(end_tile)
			end_tile.links.append(start_tile)

	def client_adjust_grid_handler(self, command):
		self.base_x += command.data['adjust_x']
		self.base_y += command.data['adjust_y']
		command.data.update({ 'base_x': self.base_x, 'base_y': self.base_y })
		self.default_handler(command)

class ClientGameState(FullClientState):
	def __init__(self, set_state, add_command, player_name, game_name, host):
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.rooms = ClientRoomGrid()
		self.players = FullServerPlayerList()
		self.current_player = False
		self.title = None
		super().__init__(set_state, add_command)
		self.children = [self.rooms]
		self.add_command(Command('redraw'))

	def redraw(self):
		if self.title:
			self.other = [
				pyglet.text.Label(
					text=self.title, 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_HEIGHT - 40, 
					anchor_x='center', 
					anchor_y='center', 
					align='center', 
					font_size=25, 
					color=(255, 255, 255, 255),
					batch=self.renderer.get_batch(),
					group=self.renderer.get_group(5)
				)
			]
		
	def redraw_handler(self, command):
		self.renderer = Renderer()
		self.redraw()
		command.data.update({ 'renderer': self.renderer })
		self.rooms.on_command(command)

	def key_press_handler(self, command):
		if command.data['symbol'] == pyglet.window.key.W:
			self.add_command(Command('client_adjust_grid', { 'adjust_x': 0, 'adjust_y': -250 }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.D:
			self.add_command(Command('client_adjust_grid', { 'adjust_x': -250, 'adjust_y': 0 }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.S:
			self.add_command(Command('client_adjust_grid', { 'adjust_x': 0, 'adjust_y': 250 }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.A:
			self.add_command(Command('client_adjust_grid', { 'adjust_x': 250, 'adjust_y': 0 }))
			self.add_command(Command('redraw'))

