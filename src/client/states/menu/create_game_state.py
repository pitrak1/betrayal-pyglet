import sys
from src.client.world.common import button as button_module, text_box as text_box_module, area as area_module, background as background_module, label as label_module
from src.client.states import state as state_module
from src.client.states.menu import main_menu_state as main_menu_state_module, game_state as game_state_module
from src.shared import constants, command as command_module

class CreateGameState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.game_name_text_box = text_box_module.TextBox(
			self.asset_manager.common['text_box'], 
			constants.WINDOW_CENTER_X - 200, 
			constants.WINDOW_CENTER_Y + 50, 
			26, 
			'Game Name'
		)
		self.password_text_box = text_box_module.TextBox(
			self.asset_manager.common['text_box'], 
			constants.WINDOW_CENTER_X - 200, 
			constants.WINDOW_CENTER_Y - 50, 
			26, 
			'Password (optional)'
		)
		self.elements = [
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
				'Create Game', 
				x=constants.WINDOW_CENTER_X,
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center', 
				anchor_y='center', 
				align='center', 
				font_size=25, 
				color=(0, 0, 0, 255)
			),
			self.game_name_text_box,
			self.password_text_box,
			button_module.Button(
				self.asset_manager.common['button'], 
				250, 
				115, 
				12, 
				3, 
				'Back', 
				lambda : self.back()
			),
			button_module.Button(
				self.asset_manager.common['button'], 
				550, 
				115, 
				12, 
				3, 
				'Create', 
				lambda : self.create()
			)
		]

	def back(self):
		self.set_state(main_menu_state_module.MainMenuState(
			{ 'assets': self.asset_manager }, 
			self.set_state, 
			self.add_command
		))

	def invalid_game_name(self):
		self.game_name_text_box.set_error_text('name is already in use')

	def create(self):
		game_name = self.game_name_text_box.get_text()
		if len(game_name) < 6:
			self.game_name_text_box.set_error_text('must be 6 characters or more')
		elif len(game_name) > 40:
			self.game_name_text_box.set_error_text('must be 40 characters or less')

		password = self.password_text_box.get_text()
		self.add_command(command_module.Command('network_create_game', { 'status': 'pending', 'game_name': game_name, 'password': password }))

	def next(self, game_name):
		self.set_state(game_state_module.GameState(
			{ 'assets': self.asset_manager, 'game_name': game_name }, 
			self.set_state, 
			self.add_command
		))