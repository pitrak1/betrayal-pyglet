from src.client.world.common import background as background_module, button as button_module, area as area_module, label as label_module
from src.client.world.menu import lobby_listing as lobby_listing_module
from src.client.states.menu import main_menu_state as main_menu_state_module, lobby_state as lobby_state_module
from src.client.states import state as state_module
from src.shared import constants, command as command_module

class LobbyListState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.starting_ui = [
			background_module.Background(self.asset_manager.menu['menu_background']),
			area_module.Area(
				self.asset_manager.common['white_button'], 
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y, 
				40, 
				30, 
				opacity=192
			),
			label_module.Label(
				'Lobbies',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(0, 0, 0, 255)
			),
			button_module.Button(
				self.asset_manager.common['brown_button'], 
				constants.WINDOW_CENTER_X - 150, 
				constants.WINDOW_CENTER_Y - 185, 
				12, 
				3, 
				'Back', 
				lambda : self.back()
			),
			button_module.Button(
				self.asset_manager.common['brown_button'], 
				constants.WINDOW_CENTER_X + 150, 
				constants.WINDOW_CENTER_Y - 185, 
				12, 
				3, 
				'Refresh', 
				lambda : self.refresh()
			)
		]
		self.elements = self.starting_ui
		self.add_command(command_module.Command('network_get_games', { 'status': 'pending' }))

	def set_lobbies(self, lobbies):
		self.elements = self.starting_ui.copy()
		count = 0
		for lobby in lobbies:
			self.elements.append(lobby_listing_module.LobbyListing(
				self.asset_manager, 
				lobby[0], 
				lobby[1], 
				constants.WINDOW_CENTER_X - 200, 
				constants.WINDOW_CENTER_Y + 120 - 30 * count, 
				lambda : self.join(lobby[0])
			))
			count += 1
			if count == 8: break

	def refresh(self):
		self.add_command(command_module.Command('network_get_games', { 'status': 'pending' }))

	def back(self):
		self.set_state(main_menu_state_module.MainMenuState(
			{ 'assets': self.asset_manager },
			self.set_state, 
			self.add_command
		))

	def join(self, lobby):
		password = 'password'
		self.add_command(command_module.Command('network_join_game', { 'status': 'pending', 'game_name': lobby, 'password': password }))

	def next(self, lobby_name):
		self.set_state(lobby_state_module.LobbyState(
			{ 'assets': self.asset_manager, 'lobby_name': lobby_name },
			self.set_state, 
			self.add_command
		))


