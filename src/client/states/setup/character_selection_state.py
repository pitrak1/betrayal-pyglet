from src.client.states.setup import character_overview_state as character_overview_state_module
from src.client.world.common import label as label_module
from src.client.world.setup import character_tile as character_tile_module
from src.client.states import state as state_module
from src.shared import constants, command as command_module
import config

class CharacterSelectionState(state_module.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)

		self.character_tiles = {}
		count = 0
		for character in config.STARTING_CHARACTERS:
			x = 68 + 132 * (count % 6)
			y = 132 + 260 * (count // 6)
			self.character_tiles[character['variable_name']] = character_tile_module.CharacterTile(self.asset_manager, character, x, y, self.select_character)
			count += 1
		
		self.title = None
		self.current_player = False

		self.elements = []
		self.add_command(command_module.Command('network_get_available_characters', { 'status': 'pending' }))

	def set_available_characters(self, characters):
		self.characters = []
		for character in characters:
			self.characters.append(self.character_tiles[character])
		self.elements = self.characters.copy()
		if self.title: self.elements.append(self.title)

		self.add_command(command_module.Command('network_get_current_player', { 'status': 'pending' }))

	def set_current_player(self, player_name):
		if player_name == 'self':
			self.title = label_module.Label('You are choosing', x=constants.WINDOW_CENTER_X, y=constants.WINDOW_HEIGHT - 40, anchor_x='center', anchor_y='center', align='center', font_size=25, color=(255, 255, 255, 255))
			self.current_player = True
		else:
			self.title = label_module.Label(f'{player_name} is choosing', x=constants.WINDOW_CENTER_X, y=constants.WINDOW_HEIGHT - 40, anchor_x='center', anchor_y='center', align='center', font_size=25, color=(255, 255, 255, 255))
			self.current_player = False

		self.elements = self.characters.copy()
		self.elements.append(self.title)

	def select_character(self, character):
		print(character)
		if self.current_player:
			self.add_command(command_module.Command('network_select_character', { 'status': 'pending', 'character': character }))

	def set_character(self, character):
		self.character = character

	def all_characters_selected(self):
		self.set_state(character_overview_state_module.CharacterOverviewState({ 'assets': self.asset_manager }, self.set_state, self.add_command))


