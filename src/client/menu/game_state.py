import sys
import pyglet
from src.client.menu import game_player, main_menu_state
from src.client.common import background, button, area, label, state
from src.client.setup import player_order_state
from src.shared import constants, command

class GameState(state.State):
	def __init__(self, asset_manager, set_state, add_command, player_name, game_name, host, testing=False):
		super().__init__(asset_manager, set_state, add_command, testing)
		self.player_name = player_name
		self.game_name = game_name
		self.host = host
		self.players = []
		self.redraw()
		self.add_command(command.Command('network_get_players_in_game', { 'status': 'pending', 'exception': None }))

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
					text=self.game_name,
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
					on_click=self.leave_game,
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

			if self.host:
				self.elements['start_button'] = button.Button(
					asset=self.asset_manager.common['button'], 
					x=constants.WINDOW_CENTER_X + 150, 
					y=constants.WINDOW_CENTER_Y - 185, 
					unit_width=12, 
					unit_height=3, 
					text='Start', 
					on_click=self.start_game,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				)

			count = 0
			for player in self.players:
				self.elements[f'player_{count}'] = game_player.GamePlayer(
					asset_manager=self.asset_manager, 
					name=player[0], 
					host=True if player[1] == 'True' else False, 
					x=constants.WINDOW_CENTER_X - 200, 
					y=constants.WINDOW_CENTER_Y + 120 - 40 * count,
					batch=self.batch,
					area_group=self.groups[2],
					text_group=self.groups[3]
				)
				count += 1


	def leave_game(self):
		self.add_command(command.Command('network_leave_game', { 'status': 'pending' }))

	def back(self):
		self.set_state(main_menu_state.MainMenuState(
			self.asset_manager, 
			self.set_state, 
			self.add_command,
			self.player_name,
			testing=self.testing
		))

	def start_game(self):
		if len(self.players) < 2:
			self.elements['error_text'].text = 'Two or more players are required'
		else:
			self.add_command(command.Command('network_start_game', { 'status': 'pending' }))

	def not_enough_players(self):
		self.elements['error_text'].text = 'Two or more players are required'

	def next(self):
		self.set_state(player_order_state.PlayerOrderState(
			self.asset_manager,
			self.set_state, 
			self.add_command,
			self.player_name,
			self.game_name,
			self.host,
			testing=self.testing
		))

	def set_players(self, players):
		self.players = players
		self.redraw()
