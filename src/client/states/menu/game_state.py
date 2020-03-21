import sys
import pyglet
from src.client.world.menu import game_player
from src.client.world.common import background, button, area, label
from src.client.states.menu import main_menu_state
from src.client.states.setup import player_order_state
from src.client.states import state
from src.shared import constants, command

class GameState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self._elements = self.__create_base_elements()
		self._add_command(command.Command('network_get_players_in_game', { 'status': 'pending', 'exception': None }))
		self.__players = []

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
		elements = [
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
				text=self._data['game_name'],
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
				on_click=self.__leave_game,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			),
			self.__error_text
		]

		if self._data['host']:
			elements.append(button.Button(
				asset=self._data['assets'].common['button'], 
				x=constants.WINDOW_CENTER_X + 150, 
				y=constants.WINDOW_CENTER_Y - 185, 
				unit_width=12, 
				unit_height=3, 
				text='Start', 
				on_click=self.__start_game,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			))

		return elements

	def __leave_game(self):
		self._add_command(command.Command('network_leave_game', { 'status': 'pending' }))

	def back(self):
		self._set_state(main_menu_state.MainMenuState(
			self._data, 
			self._set_state, 
			self._add_command
		))

	def __start_game(self):
		if len(self.__players) < 2:
			self.__error_text.text = 'Two or more players are required'
		else:
			self._add_command(command.Command('network_start_game', { 'status': 'pending' }))

	def not_enough_players(self):
		self.__error_text.text = 'Two or more players are required'

	def next(self):
		self._set_state(player_order_state.PlayerOrderState(
			self._data,
			self._set_state, 
			self._add_command
		))

	def set_players(self, players):
		self._batch = pyglet.graphics.Batch()
		self.__groups = [pyglet.graphics.OrderedGroup(i) for i in range(4)]
		self._elements = self.__create_base_elements()
		self.__players = players
		count = 0
		for player in players:
			self._elements.append(game_player.GamePlayer(
				asset_manager=self._data['assets'], 
				name=player[0], 
				host=True if player[1] == 'True' else False, 
				x=constants.WINDOW_CENTER_X - 200, 
				y=constants.WINDOW_CENTER_Y + 120 - 40 * count,
				batch=self._batch,
				area_group=self.__groups[2],
				text_group=self.__groups[3]
			))
			count += 1
