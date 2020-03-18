import sys
from src.client.world.menu import game_player as game_player_module
from src.client.world.common import background as background_module, button as button_module, area as area_module, label as label_module
from src.client.states.menu import main_menu_state as main_menu_state_module
from src.client.states.setup import player_order_state as player_order_state_module
from src.client.states import state as state_module
from src.shared import constants, command as command_module

class GameState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.game_name = data['game_name']
		self.base_ui = [
			background_module.Background(self.asset_manager.common['menu_background']),
			area_module.Area(
				self.asset_manager.common['area'], 
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y, 
				40, 
				30, 
				opacity=192
			),
			label_module.Label(
				self.game_name,
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255)
			),
			button_module.Button(
				self.asset_manager.common['button'], 
				constants.WINDOW_CENTER_X - 150, 
				constants.WINDOW_CENTER_Y - 185, 
				12, 
				3, 
				'Back', 
				lambda : self.leave_game()
			),
			button_module.Button(
				self.asset_manager.common['button'], 
				constants.WINDOW_CENTER_X + 150, 
				constants.WINDOW_CENTER_Y - 185, 
				12, 
				3, 
				'Start', 
				lambda : self.start_game()
			)
		]
		self.elements = self.base_ui
		self.add_command(command_module.Command('network_get_players_in_game', { 'status': 'pending', 'exception': None }))

	def leave_game(self):
		self.add_command(command_module.Command('network_leave_game', { 'status': 'pending' }))

	def back(self):
		self.set_state(main_menu_state_module.MainMenuState(
			{ 'assets': self.asset_manager }, 
			self.set_state, 
			self.add_command
		))

	def start_game(self):
		self.add_command(command_module.Command('network_start_game', { 'status': 'pending' }))

	def next(self):
		self.set_state(player_order_state_module.PlayerOrderState(
			{ 'assets': self.asset_manager },
			self.set_state, 
			self.add_command
		))

	def set_players(self, players):
		self.elements = self.base_ui.copy()
		count = 0
		for player in players:
			self.elements.append(game_player_module.GamePlayer(
				self.asset_manager, 
				player[0], 
				True if player[1] == 'True' else False, 
				constants.WINDOW_CENTER_X - 200, 
				constants.WINDOW_CENTER_Y + 120 - 40 * count
			))
			count += 1
