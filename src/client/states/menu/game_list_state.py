import pyglet
from src.client.world.common import background, button, area, label
from src.client.world.menu import game_listing 
from src.client.states.menu import main_menu_state, game_state
from src.client.states import state
from src.shared import constants, command

class GameListState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self._elements = self.__create_base_elements()
		self._add_command(command.Command('network_get_games', { 'status': 'pending' }))

	def __create_base_elements(self):
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(4)]
		self.__error_text = label.Label(
			text='',
			font_size=15,
			x=constants.WINDOW_CENTER_X + 150, 
			y=constants.WINDOW_CENTER_Y - 220,
			anchor_x='center',
			anchor_y='center',
			align='center',
			color=(255, 0, 0, 255),
			batch=self._batch,
			group=self.__groups[2]
		)
		return [
			background.Background(
				asset=self._data['assets'].common['menu_background'],
				batch=self._batch,
				group=self.__groups[0]
			),
			area.Area(
				asset=self._data['assets'].common['area'], 
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y, 
				unit_width=40, 
				unit_height=30, 
				opacity=192,
				batch=self._batch,
				group=self.__groups[1]
			),
			label.Label(
				text='Games',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255),
				batch=self._batch,
				group=self.__groups[2]
			),
			button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X - 150, 
				y=constants.WINDOW_CENTER_Y - 185, 
				unit_width=12, 
				unit_height=3, 
				text='Back', 
				on_click=self.__back,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			),
			button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X + 150, 
				y=constants.WINDOW_CENTER_Y - 185, 
				unit_width=12, 
				unit_height=3, 
				text='Refresh', 
				on_click=self.__refresh,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			),
			self.__error_text
		]

	def set_games(self, games):
		self.__available_games = games
		self.__available_games_count = len(games)
		self.__current_page = 0
		self.__update()

	def __go_forward_page(self):
		self.__current_page += 1
		self.__update()

	def __go_back_page(self):
		self.__current_page -= 1
		self.__update()

	def __update(self):
		self._elements = self.__create_base_elements()

		min_ = self.__current_page * constants.GAME_LIST_PAGE_SIZE
		max_ = min(self.__current_page * constants.GAME_LIST_PAGE_SIZE + constants.GAME_LIST_PAGE_SIZE, self.__available_games_count)

		count = 0
		for game in self.__available_games[min_:max_]:
			if game == '': break
			self._elements.append(game_listing.GameListing(
				asset_manager=self._data['assets'], 
				name=game[0], 
				players=game[1], 
				x=constants.WINDOW_CENTER_X - 200, 
				y=constants.WINDOW_CENTER_Y + 120 - 40 * (count % constants.GAME_LIST_PAGE_SIZE), 
				on_click=lambda : self.__join(game[0], int(game[1])),
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			))
			count += 1

		if self.__current_page * constants.GAME_LIST_PAGE_SIZE + constants.GAME_LIST_PAGE_SIZE < self.__available_games_count:
			self._elements.append(button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X + 250, 
				y=constants.WINDOW_CENTER_Y - 50, 
				unit_width=3, 
				unit_height=5, 
				text='Down', 
				on_click=self.__go_forward_page,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			))

		if self.__current_page != 0:
			self._elements.append(button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X + 250, 
				y=constants.WINDOW_CENTER_Y + 50, 
				unit_width=3, 
				unit_height=5, 
				text='Up', 
				on_click=self.__go_back_page,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			))

	def __refresh(self):
		self._add_command(command.Command('network_get_games', { 'status': 'pending' }))

	def __back(self):
		self._set_state(main_menu_state.MainMenuState(
			self._data,
			self._set_state, 
			self._add_command
		))

	def __join(self, game, number_of_players):
		if number_of_players >= constants.PLAYERS_PER_GAME:
			self.__error_text.text = 'Game is full'
		else:
			self._add_command(command.Command('network_join_game', { 'status': 'pending', 'game_name': game }))

	def game_full(self):
		self.__error_text.text = 'Game is full'

	def next(self, game_name):
		self._data.update({ 'game_name': game_name, 'host': False })
		self._set_state(game_state.GameState(
			self._data,
			self._set_state, 
			self._add_command		
		))


