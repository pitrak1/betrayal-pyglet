import pyglet
from lattice2d.client import ClientState
from src.client.components import ClientRoomGrid, ClientPlayer
from lattice2d.command import Command
from lattice2d.components import Label
from lattice2d.grid import get_distance
from constants import Constants

class BaseState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		self.rooms = ClientRoomGrid(state_machine, Constants.grid_dimensions)
		self.players = []
		self.player_name = custom_data['player_name']
		self.current_player = False
		self.title = None
		self.current_selection = None
		super().__init__(add_command, custom_data)
		self.children = [self.rooms]
		self.add_command(Command('get_player_positions', status='pending'))

	def network_get_player_positions_handler(self, command):
		if command.status == 'success':
			for player_tuple in command.data['players']:
				name, character, grid_position = player_tuple
				entry = next(c for c in Constants.characters if c['variable_name'] == character)
				player = ClientPlayer(name, add_command=self.add_command, character_entry=entry)
				self.players.append(player)
				self.rooms.add_actor(grid_position, player)
			self.add_command(Command('network_get_current_player', status='pending'))

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
			self.children = [
				self.rooms,
				Label(
					text=self.title, 
					x=Constants.window_center_x, 
					y=Constants.window_dimensions_y - 40, 
					anchor_x='center', 
					anchor_y='center', 
					align='center', 
					font_size=25, 
					color=(255, 255, 255, 255),
					batch=self.renderer.get_batch(),
					group=self.renderer.get_group(5)
				)
			]
		
	def client_select_handler(self, command):
		self.current_selection = command.data['selected']
		self.default_handler(command)

	def redraw_handler(self, command):
		self.renderer = Renderer()
		self.redraw()
		command.data.update({ 'renderer': self.renderer })
		self.rooms.on_command(command)

	def client_move_handler(self, command):
		if isinstance(self.current_selection, ClientPlayer) and get_distance(self.current_selection.grid_position, command.data['grid_position']) == 1:
			self.add_command(Command('network_move', { 
				'player': self.current_selection.name, 
				'grid_position': command.data['grid_position']			
			}, status='pending'))

	def network_move_handler(self, command):
		if command.status == 'success':
			self.rooms.move_actor(command.data['grid_position'], self.current_selection)
			self.add_command(Command('redraw'))

	def key_press_handler(self, command):
		if command.data['symbol'] == pyglet.window.key.W:
			self.add_command(Command('adjust_grid_position', { 'adjust': (0, -GRID_SIZE) }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.D:
			self.add_command(Command('adjust_grid_position', { 'adjust': (-GRID_SIZE, 0) }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.S:
			self.add_command(Command('adjust_grid_position', { 'adjust': (0, GRID_SIZE) }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.A:
			self.add_command(Command('adjust_grid_position', { 'adjust': (GRID_SIZE, 0) }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.PAGEUP or command.data['symbol'] == pyglet.window.key.UP:
			self.add_command(Command('adjust_grid_scale', { 'adjust': 2 }))
			self.add_command(Command('redraw'))
		elif command.data['symbol'] == pyglet.window.key.PAGEDOWN or command.data['symbol'] == pyglet.window.key.DOWN:
			self.add_command(Command('adjust_grid_scale', { 'adjust': 0.5 }))
			self.add_command(Command('redraw'))
