from src.client.states.setup import character_selection_state as character_selection_state_module
from src.client.states import state as state_module
from src.client.world.common import button as button_module, label as label_module
from src.shared import constants, command as command_module

class PlayerOrderState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.base_ui = [
			label_module.Label(
				'Welcome to Betrayal Online',
				font_size=25,
				x=constants.WINDOW_CENTER_X, 
				y=constants.WINDOW_CENTER_Y + 200,
				anchor_x='center',
				anchor_y='center',
				align='center',
				color=(255, 255, 255, 255)
			),
			label_module.Label(
				'Turn order will be randomly determined', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 100, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255)
			),
			label_module.Label(
				'First player in the order will play first.', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 60, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255)
			),
			label_module.Label(
				'Last player in the order will choose their character first.', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y + 40, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255)
			),
			button_module.Button(
				self.asset_manager.common['button'], 
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y - 140, 
				12, 
				3, 
				'Continue', 
				lambda : self.confirm_order()
			)
		]
		self.elements = self.base_ui
		self.add_command(command_module.Command('network_get_player_order', { 'status': 'pending' }))
		self.waiting = False

	def set_player_order(self, players):
		self.elements = self.base_ui.copy()
		self.elements.append(label_module.Label(
			'The player order is:', 
			x=constants.WINDOW_CENTER_X - 220, 
			y=constants.WINDOW_CENTER_Y - 40, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255)
		))
		player_text = ''
		for player in players:
			player_text += player
			player_text += ', '
		self.elements.append(label_module.Label(
			player_text[:-2], 
			x=constants.WINDOW_CENTER_X - 220, 
			y=constants.WINDOW_CENTER_Y - 60, 
			anchor_x='left', 
			anchor_y='center', 
			align='left', 
			font_size=15, 
			color=(255, 255, 255, 255)
		))

	def confirm_order(self):
		if not self.waiting:
			self.waiting = True
			self.elements.append(label_module.Label(
				'Waiting for other players...', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y - 200, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255)
			))
			self.add_command(command_module.Command('network_confirm_player_order', { 'status': 'pending' }))

	def next(self):
		self.set_state(character_selection_state_module.CharacterSelectionState(
			{ 'assets': self.asset_manager },
			self.set_state, 
			self.add_command
		))
