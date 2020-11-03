from lattice2d.client import ClientState
from lattice2d.components import Background, Area, Button, Label
from lattice2d.utilities import get_page_info
from lattice2d.command import Command
from src.client.menu_states.game_listing import GameListing
from constants import WINDOW_CENTER, GAME_LIST_PAGE_SIZE, PLAYERS_PER_GAME

class GameListState(ClientState):
	def __init__(self, state_machine, custom_data={}):
		self.__current_page = 0
		self.__available_games = []
		self.__available_games_count = 0
		super().__init__(state_machine, custom_data)
		self.add_command(Command('get_games', status='pending'))
		self.register_component('background', 'background', Background('menu_background'))
		self.register_component('area', 'base', Area(
			position=(WINDOW_CENTER[0], WINDOW_CENTER[1]),
			unit_dimensions=(20, 15)
		))
		self.register_component('back_button', 'ui', Button(
			position=(WINDOW_CENTER[0] - 150, WINDOW_CENTER[1] - 185),
			unit_dimensions=(12, 3),
			text='Back',
			on_click=self.back
		))
		self.register_component('refresh', 'ui', Button(
			position=(WINDOW_CENTER[0] + 150, WINDOW_CENTER[1] - 185),
			unit_dimensions=(12, 3),
			text='Refresh',
			on_click=self.refresh
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
		self.register_component('title', 'ui', Label(
			text='Games',
			font_size=25,
			x=WINDOW_CENTER[0],
			y=WINDOW_CENTER[1] + 200,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(0, 0, 0, 255)
		))

	def __redraw(self):
		if self.__available_games_count > 0:
			for count in range(0, GAME_LIST_PAGE_SIZE):
				self.conditionally_remove_component(f'game_{count}')
			self.conditionally_remove_component('down_button')
			self.conditionally_remove_component('up_button')

			min_, max_, down, up = get_page_info(
				self.__current_page, 
				GAME_LIST_PAGE_SIZE, 
				self.__available_games_count
			)

			count = 0
			for game in self.__available_games[min_:max_]:
				if game == '': break
				self.register_component(f'game_{count}', 'ui', GameListing(
					name=game[0], 
					players=game[1], 
					position=(WINDOW_CENTER[0] - 200, WINDOW_CENTER[1] + 120 - 40 * (count % GAME_LIST_PAGE_SIZE)), 
					on_click=lambda : self.join(game[0], int(game[1]))
				))
				count += 1

			if down:
				self.register_component('down_button', 'ui', Button(
					position=(WINDOW_CENTER[0] + 250, WINDOW_CENTER[1] - 50), 
					unit_dimensions=(2, 3), 
					text='Down', 
					on_click=self.go_forward_page
				))

			if up:
				self.register_component('up_button', 'ui', Button(
					position=(WINDOW_CENTER[0] + 250, WINDOW_CENTER[1] + 50),
					unit_dimensions=(2, 3),
					text='Up',
					on_click=self.go_back_page
				))

	def get_games_handler(self, command):
		if command.status == 'success':
			self.__available_games = command.data['games']
			self.__available_games_count = len(command.data['games'])
			self.__redraw()

	def go_forward_page(self):
		self.__current_page += 1
		self.__redraw()

	def go_back_page(self):
		self.__current_page -= 1
		self.__redraw()

	def refresh(self):
		self.add_command(Command('get_games', status='pending'))

	def back(self):
		self.to_main_menu_state(self.custom_data)

	def join(self, game, number_of_players):
		if number_of_players >= PLAYERS_PER_GAME:
			self.get_component('error_label').text = 'Game is full'
		else:
			self.add_command(Command('join_game', { 'game_name': game }, 'pending'))

	def join_game_handler(self, command):
		if command.status == 'game_full':
			self.get_component('error_label').text = 'Game is full'
		elif command.status == 'success':
			self.custom_data.update({ 'game_name': command.data['game_name'], 'host': False })
			self.to_lobby_state(self.custom_data)
