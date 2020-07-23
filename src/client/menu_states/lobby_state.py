from lattice2d.client.client_state import ClientState
from lattice2d.client.components.background import Background
from lattice2d.client.components.area import Area
from lattice2d.client.components.button import Button
from lattice2d.client.components.label import Label
from lattice2d.network.network_command import NetworkCommand
from lattice2d.client.renderer import Renderer
from src.client.menu_states.game_player import GamePlayer
from constants import WINDOW_CENTER, MINIMUM_PLAYERS

class LobbyState(ClientState):
	def __init__(self, add_command, custom_data={}):
		self.players = []
		super().__init__(add_command, custom_data)
		self.add_command(NetworkCommand('broadcast_players_in_game', status='pending'))

	def redraw(self):
		self.error_text = Label(
			text='',
			font_size=15,
			x=WINDOW_CENTER[0] + 150, 
			y=WINDOW_CENTER[1] - 220,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(255, 0, 0, 255),
			batch=self.renderer.get_batch(),
			group=self.renderer.get_group(2)
		)
		self.children = [
			Background(
				asset_key='menu_background',
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(0)
			),
			Area(
				position=(WINDOW_CENTER[0], WINDOW_CENTER[1]), 
				unit_dimensions=(20, 15), 
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(1)
			),
			Button(
				position=(WINDOW_CENTER[0] - 150, WINDOW_CENTER[1] - 185), 
				unit_dimensions=(6, 2), 
				text='Back', 
				on_click=self.leave_game,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Label(
				text=self.custom_data['game_name'],
				font_size=25,
				x=WINDOW_CENTER[0], 
				y=WINDOW_CENTER[1] + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self.renderer.get_batch(),
				group=self.renderer.get_group(2)
			),
			self.error_text
		]
		
		if self.custom_data['host']:
			self.children.append(Button(
				position=(WINDOW_CENTER[0] + 150, WINDOW_CENTER[1] - 185), 
				unit_dimensions=(6, 2), 
				text='Start', 
				on_click=self.start_game,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			))

		count = 0
		for player in self.players:
			self.children.append(GamePlayer(
				name=player[0], 
				host=player[1], 
				position=(WINDOW_CENTER[0] - 200, WINDOW_CENTER[1] + 120 - 40 * count),
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			))
			count += 1

	def broadcast_players_in_game_handler(self, command):
		if command.status == 'success':
			self.players = command.data['players']
			self.renderer = Renderer()
			self.redraw()

	def leave_game(self):
		self.add_command(NetworkCommand('leave_game', status='pending'))

	def leave_game_handler(self, command):
		if command.status == 'success':
			self.to_main_menu_state(self.custom_data)

	def start_game(self):
		if len(self.players) < MINIMUM_PLAYERS:
			self.error_text.text = 'Two or more players are required'
		else:
			self.add_command(NetworkCommand('network_start_game', status='pending'))

	def network_start_game_handler(self, command):
		if command.status == 'not_enough_players':
			self.error_text.text = 'Two or more players are required'
		else:
			self.to_player_order_state(self.custom_data)
