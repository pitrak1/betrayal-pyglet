import sys
from src.client.world.common import background as background_module, button as button_module, area as area_module, label as label_module
from src.client.states import state as state_module
from src.client.states.menu import create_lobby_state as create_lobby_state_module, lobby_list_state as lobby_list_state_module
from src.shared import constants, command as command_module

class MainMenuState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
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
			button_module.Button(
				self.asset_manager.common['brown_button'],
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y + 50, 
				12, 
				3, 
				'Create Game', 
				lambda : self.create_lobby()
			),
			button_module.Button(
				self.asset_manager.common['brown_button'], 
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y - 30, 
				12, 
				3, 
				'Join Game', 
				lambda : self.join_lobby()
			),
			button_module.Button(
				self.asset_manager.common['brown_button'], 
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y - 110, 
				12, 
				3, 
				'Exit', 
				lambda : self.start_exit()
			)
		]

	def start_exit(self):
		self.add_command(command_module.Command('network_logout', { status: 'pending' }))

	def exit(self):
		sys.exit()

	def create_lobby(self):
		self.set_state(create_lobby_state_module.CreateLobbyState(
			{ 'assets': self.asset_manager },
			self.set_state, 
			self.add_command
		))

	def join_lobby(self):
		self.set_state(lobby_list_state_module.LobbyListState(
			{ 'assets': self.asset_manager },
			self.set_state, 
			self.add_command
		))

	

