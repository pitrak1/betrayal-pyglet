import random
import pyglet
from src.server.states import game_state as game_state_module, state
from src.shared import command as command_module, threaded_sync, logger
import config

class CharacterSelectionState(state.State):
	def __init__(self, game):
		super().__init__(game)
		random.shuffle(self.game.players)
		self.waiting = threaded_sync.ThreadedSync(len(self.game.players))
		self.current_player_index = len(self.game.players) - 1
		self.characters = []
		for character in config.CHARACTERS:
			self.characters.append(character['variable_name'])

	def network_get_player_order_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		parsed_players = [p.name for p in self.game.players]
		command_module.update_and_send(command, { 'status': 'success', 'players': parsed_players })

	def network_confirm_player_order_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		self.waiting.count()
		if self.waiting.done():
			logger.log(f'Character Selection State {self.game.name} done waiting', logger.LOG_LEVEL_DEBUG)
			command_module.update_and_send_to_all(command, { 'status': 'success' }, self.game.players)

	def network_get_available_characters_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		command_module.update_and_send(command, { 'status': 'success', 'characters': self.characters })

	def network_get_current_player_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		if command.data['connection'] == self.game.players[self.current_player_index]:
			player_name = 'self'
		else:
			player_name = self.game.players[self.current_player_index].name
		command_module.update_and_send(command, { 'status': 'success', 'player_name': player_name })

	def network_select_character_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		if command.data['connection'] == self.game.players[self.current_player_index]:
			logger.log(f'Character Selection State {self.game.name} receiving select from current player', logger.LOG_LEVEL_DEBUG)
			character_entry = next(character for character in config.CHARACTERS if character['variable_name'] == command.data['character'])
			self.game.players[self.current_player_index].set_character(character_entry)
			self.characters = [x for x in self.characters if x != character_entry['variable_name'] and x not in character_entry['related']]

			self.current_player_index -= 1
			if self.current_player_index < 0:
				command_module.create_and_send_to_all(
					'network_all_characters_selected',
					{ 'status': 'success' },
					self.game.players
				)
			else:
				command_module.create_and_send_to_all(
					'network_get_current_player',
					{ 'status': 'success', 'player_name': self.game.players[self.current_player_index].name },
					self.game.players
				)
				command_module.create_and_send_to_all(
					'network_get_available_characters',
					{ 'status': 'success', 'characters': self.characters },
					self.game.players
				)

	def network_get_character_selections_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		selections = [(p.name, p.display_name) for p in self.game.players]
		command_module.update_and_send(command, { 'status': 'success', 'selections': selections })

	def network_confirm_character_selections_handler(self, command, state=None):
		logger.log(f'Character Selection State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		self.waiting.count()
		if self.waiting.done():
			logger.log(f'Character Selection State {self.game.name} done waiting', logger.LOG_LEVEL_DEBUG)
			self.set_state(game_state_module.GameState(self.game))
			command_module.update_and_send_to_all(command, { 'status': 'success' }, self.game.players)
