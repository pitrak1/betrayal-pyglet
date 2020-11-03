from lattice2d.client import ClientState
from lattice2d.components import Background, Area, Button, Label
from lattice2d.command import Command
from src.client.menu_states.game_player import GamePlayer
from constants import WINDOW_CENTER, MINIMUM_PLAYERS

class LobbyState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		self.players = []
		super().__init__(state_machine, custom_data)
		self.add_command(Command('broadcast_players_in_game', status='pending'))
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1]),
			unit_dimensions=(20, 15)
		))
		self.register_component('back_button', 'ui', Button(
			position=(WINDOW_CENTER[0] - 150, WINDOW_CENTER[1] - 185),
			unit_dimensions=(12, 3),
			text='Back',
			on_click=self.leave_game
		))
		self.register_component('title', 'ui', Label(
			text=self.custom_data['game_name'],
			font_size=25,
			x=WINDOW_CENTER[0],
			y=WINDOW_CENTER[1] + 200,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(0, 0, 0, 255)
		))
		self.register_component('error_label', 'ui', Label(
			text='',
			font_size=15,
			x=WINDOW_CENTER[0] + 150,
			y=WINDOW_CENTER[1] - 220,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(255, 0, 0, 255)
		))
		if self.custom_data['host']:
			self.register_component('start_button', 'ui', Button(
				position=(WINDOW_CENTER[0] + 150, WINDOW_CENTER[1] - 185),
				unit_dimensions=(12, 3),
				text='Start',
				on_click=self.start_game
			))
		self.__draw_players()

	def __draw_players(self):
		for count in range(0, 10):
			self.conditionally_remove_component(f'player_{count}')

		count = 0
		for player in self.players:
			self.register_component(f'player_{count}', 'ui', GamePlayer(
				name=player[0], 
				host=player[1], 
				position=(WINDOW_CENTER[0] - 200, WINDOW_CENTER[1] + 120 - 80 * count)
			))
			count += 1

	def broadcast_players_in_game_handler(self, command):
		if command.status == 'success':
			self.players = command.data['players']
			self.__draw_players()

	def leave_game(self):
		self.add_command(Command('leave_game', status='pending'))

	def leave_game_handler(self, command):
		if command.status == 'success':
			self.to_main_menu_state(self.custom_data)

	def start_game(self):
		if len(self.players) < MINIMUM_PLAYERS:
			self.get_component('error_label').text = 'Two or more players are required'
		else:
			self.add_command(Command('network_start_game', status='pending'))

	def network_start_game_handler(self, command):
		if command.status == 'not_enough_players':
			self.get_component('error_label').text = 'Two or more players are required'
		else:
			self.to_player_order_state(self.custom_data)
