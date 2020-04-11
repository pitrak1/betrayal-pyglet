import pyglet
from src.client.common import background, button, area, label, state
from src.client.menu import game_listing, main_menu_state, game_state
from src.shared import constants, command, pagination

class GameListState(state.State):
	def __init__(self, asset_manager, set_state, add_command, player_name, testing=False):
		super().__init__(asset_manager, set_state, add_command, testing)
		self.player_name = player_name
		self.current_page = 0
		self.available_games = []
		self.available_games_count = 0
		self.redraw()
		self.add_command(command.Command('network_get_games', { 'status': 'pending' }))

	def redraw(self):
		if not self.testing:
			self.batch = pyglet.graphics.Batch()
			self.groups = [pyglet.graphics.OrderedGroup(i) for i in range(4)]
			self.elements = {
				'background': background.Background(
					asset=self.asset_manager.common['menu_background'],
					batch=self.batch,
					group=self.groups[0]
				),
				'border': area.Area(
					asset=self.asset_manager.common['area'], 
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y, 
					unit_width=40, 
					unit_height=30, 
					opacity=192,
					batch=self.batch,
					group=self.groups[1]
				),
				'title': label.Label(
					text='Games',
					font_size=25,
					x=constants.WINDOW_CENTER_X, 
					y=constants.WINDOW_CENTER_Y + 200,
					anchor_x='center',
					anchor_y='center',
					align='center',
					color=(0, 0, 0, 255),
					batch=self.batch,
					group=self.groups[2]
				),
				'back_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X - 150, 
					y=constants.WINDOW_CENTER_Y - 185, 
					unit_width=12, 
					unit_height=3, 
					text='Back', 
					on_click=self.back,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				),
				'refresh_button': button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X + 150, 
					y=constants.WINDOW_CENTER_Y - 185, 
					unit_width=12, 
					unit_height=3, 
					text='Refresh', 
					on_click=self.refresh,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				),
				'error_text': label.Label(
					text='',
					font_size=15,
					x=constants.WINDOW_CENTER_X + 150, 
					y=constants.WINDOW_CENTER_Y - 220,
					anchor_x='center',
					anchor_y='center',
					align='center',
					color=(255, 0, 0, 255),
					batch=self.batch,
					group=self.groups[2]
				)
			}

			if self.available_games_count > 0:
				min_, max_, down, up = pagination.get_page_info(
					self.current_page, 
					constants.GAME_LIST_PAGE_SIZE, 
					self.available_games_count
				)

				count = 0
				for game in self.available_games[min_:max_]:
					if game == '': break
					self.elements[f'game_{count}'] = game_listing.GameListing(
						asset_manager=self.asset_manager, 
						name=game[0], 
						players=game[1], 
						x=constants.WINDOW_CENTER_X - 200, 
						y=constants.WINDOW_CENTER_Y + 120 - 40 * (count % constants.GAME_LIST_PAGE_SIZE), 
						on_click=lambda : self.join(game[0], int(game[1])),
						batch=self.batch,
						area_group=self.groups[2],
						text_group=self.groups[3]
					)
					count += 1

				if down:
					self.elements['down_button'] = button.Button(
						asset=self.asset_manager.common['button'], 
						x=constants.WINDOW_CENTER_X + 250, 
						y=constants.WINDOW_CENTER_Y - 50, 
						unit_width=3, 
						unit_height=5, 
						text='Down', 
						on_click=self.go_forward_page,
						batch=self.batch,
						area_group=self.groups[2],
						text_group=self.groups[3]
					)

				if up:
					self.elements['up_button'] = button.Button(
						asset=self.asset_manager.common['button'], 
						x=constants.WINDOW_CENTER_X + 250, 
						y=constants.WINDOW_CENTER_Y + 50, 
						unit_width=3, 
						unit_height=5, 
						text='Up', 
						on_click=self.go_back_page,
						batch=self.batch,
						area_group=self.groups[2],
						text_group=self.groups[3]
					)

	def set_games(self, games):
		self.available_games = games
		self.available_games_count = len(games)
		self.redraw()

	def go_forward_page(self):
		self.current_page += 1
		self.redraw()

	def go_back_page(self):
		self.current_page -= 1
		self.redraw()

	def refresh(self):
		self.add_command(command.Command('network_get_games', { 'status': 'pending' }))

	def back(self):
		self.set_state(main_menu_state.MainMenuState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.player_name,
			testing=self.testing
		))

	def join(self, game, number_of_players):
		if number_of_players >= constants.PLAYERS_PER_GAME:
			self.elements['error_text'].text = 'Game is full'
		else:
			self.add_command(command.Command('network_join_game', { 'status': 'pending', 'game_name': game }))

	def game_full(self):
		self.elements['error_text'].text = 'Game is full'

	def next(self, game_name):
		self.set_state(game_state.GameState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.player_name,
			game_name,
			False,
			testing=self.testing	
		))


