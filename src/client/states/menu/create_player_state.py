import sys
from src.client.world.common import background as background_module, button as button_module, text_box as text_box_module, area as area_module, label as label_module
from src.client.states import state as state_module
from src.client.states.menu import main_menu_state as main_menu_state_module
from src.shared import constants, command as command_module

class CreatePlayerState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.player_name_text_box = text_box_module.TextBox(
			self.asset_manager.common['brown_button'], 
			constants.WINDOW_CENTER_X - 120, 
			constants.WINDOW_CENTER_Y + 50, 
			16,
			'Player Name'
		)
		self.elements = [
			background_module.Background(self.asset_manager.common['menu_background']),
			area_module.Area(
				self.asset_manager.common['white_button'],
				constants.WINDOW_CENTER_X,
				constants.WINDOW_CENTER_Y,
				20,
				30,
				opacity=192
			),
			label_module.Label(
				'Betrayal Online',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 150,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255)
			),
			self.player_name_text_box,
			button_module.Button(
				self.asset_manager.common['brown_button'], 
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y - 50, 
				12, 
				3, 
				'Continue', 
				lambda : self.submit()
			),
			button_module.Button(
				self.asset_manager.common['brown_button'], 
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y - 110, 
				12, 
				3, 
				'Exit', 
				lambda : self.exit()
			)
		]

	def exit(self):
		sys.exit()

	def submit(self):
		player_name = self.player_name_text_box.get_text()
		if len(player_name) < 6:
			self.player_name_text_box.set_error_text('must be 6 characters or more')
		elif len(player_name) > 25:
			self.player_name_text_box.set_error_text('must be 25 characters or less')
		else:
			self.add_command(command_module.Command('network_create_player', { 'status': 'pending', 'player_name': player_name }))

	def invalid_player_name(self):
		self.player_name_text_box.set_error_text('name is already in use')

	def next(self):
		self.set_state(main_menu_state_module.MainMenuState(
			{ 'assets': self.asset_manager },
			self.set_state, 
			self.add_command
		))
