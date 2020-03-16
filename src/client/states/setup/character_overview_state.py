from src.client.states import state as state_module
from src.client.states.game import game_state as game_state_module
from src.client.world.common import button as button_module, label as label_module
from src.shared import constants, command as command_module

class CharacterOverviewState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.base_ui = [
			label_module.Label('The players\' selected characters are:', x=constants.WINDOW_CENTER_X, y=constants.WINDOW_HEIGHT - 40, anchor_x='center', anchor_y='center', align='center', font_size=25, color=(255, 255, 255, 255)),
			button_module.Button(
				self.asset_manager.common['brown_button'], 
				constants.WINDOW_CENTER_X, 
				constants.WINDOW_CENTER_Y - 200, 
				12, 
				3, 
				'Begin', 
				lambda : self.confirm_characters()
			)
		]
		self.elements = self.base_ui.copy()
		self.add_command(command_module.Command('network_get_character_selections', { 'status': 'pending' }))
		self.waiting = False

	def set_character_selections(self, selections):
		self.elements = self.base_ui.copy()
		count = 0
		for selection in selections:
			label_text = f'{selection[0]}: {selection[1]}'
			self.elements.append(label_module.Label(label_text, x=constants.WINDOW_CENTER_X - 180, y=constants.WINDOW_CENTER_Y + 130 - (40 * count), anchor_x='left', anchor_y='center', align='left', font_size=18, color=(255, 255, 255, 255)))
			count += 1

	def confirm_characters(self):
		if not self.waiting:
			self.waiting = True
			self.elements.append(label_module.Label(
				'Waiting for other players...', 
				x=constants.WINDOW_CENTER_X - 220, 
				y=constants.WINDOW_CENTER_Y - 260, 
				anchor_x='left', 
				anchor_y='center', 
				align='left', 
				font_size=15, 
				color=(255, 255, 255, 255)
			))
			self.add_command(command_module.Command('network_confirm_character_selections', { 'status': 'pending' }))

	def next(self):
		self.set_state(game_state_module.GameState({ 'assets': self.asset_manager }, self.set_state, self.add_command))
