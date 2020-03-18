import random
from src.server import server_character
from src.server.states import state, game_state as game_state_module
from src.shared import command as command_module, threaded_sync
import config

class CharacterSelectionState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		random.shuffle(self.players)
		self.waiting = threaded_sync.ThreadedSync(len(self.players))
		self.current_player_index = len(self.players) - 1
		self.characters = []
		for character in config.CHARACTERS:
			self.characters.append(server_character.ServerCharacter(character))

	def network_get_player_order_handler(self, command, state=None):
		parsed_players = [p.name for p in self.players]
		command_module.update_and_send(command, { 'status': 'success', 'players': parsed_players })

	def network_confirm_player_order_handler(self, command, state=None):
		self.waiting.count()
		if self.waiting.done():
			for player in self.players:
				command_module.update_and_send(command, { 'status': 'success', 'connection': player.connection })

	def network_get_available_characters_handler(self, command, state=None):
		command_module.update_and_send(command, { 'status': 'success', 'characters': [character.variable_name for character in self.characters] })

	def network_get_current_player_handler(self, command, state=None):
		if command.data['connection'] == self.players[self.current_player_index]:
			player_name = 'self'
		else:
			player_name = self.players[self.current_player_index].name
		command_module.update_and_send(command, { 'status': 'success', 'player_name': player_name })

	def network_select_character_handler(self, command, state=None):
		if command.data['connection'] == self.players[self.current_player_index]:
			self.players[self.current_player_index].character = next(character for character in self.characters if character.variable_name == command.data['character'])
			self.characters = [x for x in self.characters if x.variable_name != command.data['character'] and command.data['character'] not in x.related]
			command_module.update_and_send(command, { 'status': 'success' })

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
						{ 'status': 'success', 'characters': [character.variable_name for character in self.characters], 'connection': player.connection }
					)
		else:
			command_module.update_and_send(command, { 'status': 'not_current_player' })

	def network_get_character_selections_handler(self, command, state=None):
		selections = [(p.name, p.character.display_name if p.character else None) for p in self.players]
		command_module.update_and_send(command, { 'status': 'success', 'selections': selections })

	def network_confirm_character_selections_handler(self, command, state=None):
		self.waiting.count()
		if self.waiting.done():
			self.set_state(game_state_module.GameState(
				{ 'players': self.players, 'rooms': self.rooms }, 
				self.set_state, 
				self.add_command
			))
			for player in self.players:
				command_module.update_and_send(command, { 'status': 'success', 'connection': player.connection })
