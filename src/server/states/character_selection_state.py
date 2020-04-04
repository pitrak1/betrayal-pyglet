import random
import pyglet
from src.server.states import state, game_state as game_state_module
from src.shared import command as command_module, threaded_sync, logger
import config

class CharacterSelectionState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.name = data['name']
		random.shuffle(self.players)
		self.waiting = threaded_sync.ThreadedSync(len(self.players))
		self.current_player_index = len(self.players) - 1
		self.characters = []
		for character in config.CHARACTERS:
			self.characters.append(character['variable_name'])

	def network_get_player_order_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.name} handling command', logger.LOG_LEVEL_COMMAND)
		parsed_players = [p.name for p in self.players]
		command_module.update_and_send(command, { 'status': 'success', 'players': parsed_players })

	def network_confirm_player_order_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.name} handling command', logger.LOG_LEVEL_COMMAND)
		self.waiting.count()
		if self.waiting.done():
			logger.log(f'Character Selection State {self.name} done waiting', logger.LOG_LEVEL_DEBUG)
			for player in self.players:
				command_module.update_and_send(command, { 'status': 'success', 'connection': player.connection })

	def network_get_available_characters_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.name} handling command', logger.LOG_LEVEL_COMMAND)
		command_module.update_and_send(command, { 'status': 'success', 'characters': self.characters })

	def network_get_current_player_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.name} handling command', logger.LOG_LEVEL_COMMAND)
		if command.data['connection'] == self.players[self.current_player_index]:
			player_name = 'self'
		else:
			player_name = self.players[self.current_player_index].name
		command_module.update_and_send(command, { 'status': 'success', 'player_name': player_name })

	def network_select_character_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.name} handling command', logger.LOG_LEVEL_COMMAND)
		if command.data['connection'] == self.players[self.current_player_index]:
			logger.log(f'Character Selection State {self.name} receiving select from current player', logger.LOG_LEVEL_DEBUG)
			character_entry = next(character for character in config.CHARACTERS if character['variable_name'] == command.data['character'])
			self.players[self.current_player_index].set_character(character_entry)
			self.characters = [x for x in self.characters if x != character_entry['variable_name'] and x not in character_entry['related']]

			self.current_player_index -= 1
			if self.current_player_index < 0:
				for player in self.players:
					command_module.create_and_send(
						'network_all_characters_selected',
						{ 'status': 'success', 'connection': player.connection }
					)
			else:
				for player in self.players:
					command_module.create_and_send(
						'network_get_current_player',
						{ 'status': 'success', 'player_name': self.players[self.current_player_index].name, 'connection': player.connection }
					)
					command_module.create_and_send(
						'network_get_available_characters',
						{ 'status': 'success', 'characters': self.characters, 'connection': player.connection }
					)

	def network_get_character_selections_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.name} handling command', logger.LOG_LEVEL_COMMAND)
		selections = [(p.name, p.display_name) for p in self.players]
		command_module.update_and_send(command, { 'status': 'success', 'selections': selections })

	def network_confirm_character_selections_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.name} handling command', logger.LOG_LEVEL_COMMAND)
		self.waiting.count()
		if self.waiting.done():
			logger.log(f'Character Selection State {self.name} done waiting', logger.LOG_LEVEL_DEBUG)
			self.set_state(game_state_module.GameState(
				{ 'players': self.players, 'rooms': self.rooms, 'name': self.name }, 
				self.set_state, 
				self.add_command
			))
			for player in self.players:
				command_module.update_and_send(command, { 'status': 'success', 'connection': player.connection })
