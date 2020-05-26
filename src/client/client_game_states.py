import pyglet
import sys
from lattice2d.full.full_client import FullClientState, Renderer
from lattice2d.full.common import FullPlayerList
from lattice2d.network import NetworkCommand
from lattice2d.nodes import Command
from src.client.client_components import Background, Area, Button, TextBox
from src.client.asset_manager import Assets
from src.client.client_grid import ClientRoomGrid, ClientRoom, ClientPlayer
from src.common import constants
import config

class ClientGameState(FullClientState):
	def __init__(self, set_state, add_command, player_name, game_name, host):
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.rooms = ClientRoomGrid()
		self.players = FullPlayerList()
		self.current_player = False
		self.title = None
		super().__init__(set_state, add_command)
		self.children = [self.rooms]
		self.add_command(NetworkCommand('network_get_player_positions', status='pending'))

	def network_get_player_positions_handler(self, command):
		if command.status == 'success':
			for player_tuple in command.data['players']:
				name, character, grid_x, grid_y = player_tuple
				entry = next(c for c in config.CHARACTERS if c['variable_name'] == character)
				player = ClientPlayer(name, entry=entry)
				self.players.append(player)
				self.rooms.add_actor(grid_x, grid_y, player)
			self.add_command(NetworkCommand('network_get_current_player', status='pending'))

	def network_get_current_player_handler(self, command):
		if command.status == 'success':
			player_name = command.data['player_name']
			if player_name == self.player_name:
				self.title = 'Your turn'
				self.current_player = True
			else:
				self.title = f'{player_name}\'s turn'
				self.current_player = False

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
			self.add_command(Command('adjust_grid_position', { 'adjust_x': 0, 'adjust_y': -constants.GRID_SIZE }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.D:
			self.add_command(Command('adjust_grid_position', { 'adjust_x': -constants.GRID_SIZE, 'adjust_y': 0 }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.S:
			self.add_command(Command('adjust_grid_position', { 'adjust_x': 0, 'adjust_y': constants.GRID_SIZE }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.A:
			self.add_command(Command('adjust_grid_position', { 'adjust_x': constants.GRID_SIZE, 'adjust_y': 0 }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.PAGEUP or command.data['symbol'] == pyglet.window.key.UP:
			self.add_command(Command('adjust_grid_scale', { 'adjust': 2 }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.PAGEDOWN or command.data['symbol'] == pyglet.window.key.DOWN:
			self.add_command(Command('adjust_grid_scale', { 'adjust': 0.5 }))
			self.add_command(Command('redraw'))
