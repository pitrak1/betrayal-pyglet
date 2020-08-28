from lattice2d.client.client_state import ClientState
from lattice2d.client.components.background import Background
from lattice2d.client.components.area import Area
from lattice2d.client.components.button import Button
from lattice2d.client.components.label import Label
from lattice2d.utilities.get_page_info import get_page_info
from lattice2d.network.network_command import NetworkCommand
from lattice2d.client.renderer import Renderer
from src.client.menu_states.game_listing import GameListing
from constants import WINDOW_CENTER, GAME_LIST_PAGE_SIZE, PLAYERS_PER_GAME

class GameListState(ClientState):
	def __init__(self, add_command, custom_data={}):
		self.current_page = 0
		self.available_games = []
		self.available_games_count = 0
		super().__init__(add_command, custom_data)
		self.add_command(NetworkCommand('get_games', status='pending'))

	def redraw(self):
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
				unit_dimensions=(12, 3), 
				text='Back', 
				on_click=self.back,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			),
			Button(
				position=(WINDOW_CENTER[0] + 150, WINDOW_CENTER[1] - 185), 
				unit_dimensions=(12, 3), 
				text='Refresh', 
				on_click=self.refresh,
				batch=self.renderer.get_batch(),
				area_group=self.renderer.get_group(2),
				text_group=self.renderer.get_group(3)
			)
		]
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
		self.other = [
			Label(
				text='Games',
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

		if self.available_games_count > 0:
			min_, max_, down, up = get_page_info(
				self.current_page, 
				GAME_LIST_PAGE_SIZE, 
				self.available_games_count
			)

			count = 0
			for game in self.available_games[min_:max_]:
				if game == '': break
				self.children.append(GameListing(
					name=game[0], 
					players=game[1], 
					position=(WINDOW_CENTER[0] - 200, WINDOW_CENTER[1] + 120 - 40 * (count % GAME_LIST_PAGE_SIZE)), 
					on_click=lambda : self.join(game[0], int(game[1])),
					batch=self.renderer.get_batch(),
					area_group=self.renderer.get_group(2),
					text_group=self.renderer.get_group(3)
				))
				count += 1

			if down:
				self.elements.append(Button(
					position=(WINDOW_CENTER[0] + 250, WINDOW_CENTER[1] - 50), 
					unit_dimensions=(2, 3), 
					text='Down', 
					on_click=self.go_forward_page,
					batch=self.renderer.get_batch(),
					area_group=self.renderer.get_group(2),
					text_group=self.renderer.get_group(3)
				))

			if up:
				self.elements.append(Button(
					position=(WINDOW_CENTER[0] + 250, WINDOW_CENTER[1] + 50), 
					unit_dimensions=(2, 3), 
					text='Up', 
					on_click=self.go_back_page,
					batch=self.renderer.get_batch(),
					area_group=self.renderer.get_group(2),
					text_group=self.renderer.get_group(3)
				))

	def get_games_handler(self, command):
		if command.status == 'success':
			self.available_games = command.data['games']
			self.available_games_count = len(command.data['games'])
			self.renderer = Renderer()
			self.redraw()

	def go_forward_page(self):
		self.current_page += 1
		self.renderer = Renderer()
		self.redraw()

	def go_back_page(self):
		self.current_page -= 1
		self.renderer = Renderer()
		self.redraw()

	def refresh(self):
		self.add_command(NetworkCommand('get_games', status='pending'))

	def back(self):
		self.to_main_menu_state(self.custom_data)

	def join(self, game, number_of_players):
		if number_of_players >= PLAYERS_PER_GAME:
			self.error_text.text = 'Game is full'
		else:
			self.add_command(NetworkCommand('join_game', { 'game_name': game }, 'pending'))

	def join_game_handler(self, command):
		if command.status == 'game_full':
			self.error_text.text = 'Game is full'
		elif command.status == 'success':
			self.custom_data.update({ 'game_name': command.data['game_name'], 'host': False })
			self.to_lobby_state(self.custom_data)
