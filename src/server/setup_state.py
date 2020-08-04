import random
from lattice2d.server.server_state import ServerState
from lattice2d.grid.tile_grid import TileGrid
from lattice2d.grid.grid_navigation import get_distance
from lattice2d.network.network_command import NetworkCommand
from lattice2d.utilities.threaded_sync import ThreadedSync
from lattice2d.nodes.node import Node
from src.server.server_grid import ServerRoomGrid
from constants import CHARACTERS

class SetupState(ServerState):
	def __init__(self, game, custom_data={}):
		super().__init__(game, custom_data)
		random.shuffle(self.game.players)
		self.waiting = ThreadedSync(len(self.game.players))
		self.game.current_player_index = len(self.game.players) - 1
		self.characters = []
		for character in CHARACTERS:
			self.characters.append(character['variable_name'])

	def network_get_player_order_handler(self, command):
		parsed_players = [player.name for player in self.game.players]
		command.update_and_send(status='success', data={ 'players': parsed_players })

	def network_confirm_player_order_handler(self, command):
		self.waiting.count()
		if self.waiting.done():
			for player in self.game.players:
				command.update_and_send(status='success', connection=player.connection)

	def network_get_available_characters_handler(self, command):
		command.update_and_send(status='success', data={ 'characters': self.characters })

	def network_select_character_handler(self, command):
		if self.game.is_current_player(command):
			current_player = self.game.get_current_player()
			character_entry = next(character for character in CHARACTERS if character['variable_name'] == command.data['character'])
			current_player.set_character(character_entry)
			self.characters = [x for x in self.characters if x != character_entry['variable_name'] and x not in character_entry['related']]

			self.game.current_player_index -= 1
			current_player = self.game.get_current_player()
			if self.game.current_player_index < 0:
				for player in self.game.players:
					NetworkCommand.create_and_send('network_all_characters_selected', {}, 'success', player.connection)
			else:
				for player in self.game.players:
					NetworkCommand.create_and_send('network_get_available_characters', { 'characters': self.characters }, 'success', player.connection)

	def network_get_character_selections_handler(self, command):
		selections = [(p.character_entry['variable_name'], p.character_entry['display_name']) for p in self.game.players]
		command.update_and_send(status='success', data={ 'selections': selections })

	def network_confirm_character_selections_handler(self, command):
		self.waiting.count()
		if self.waiting.done():
			self.to_game_state()
			for player in self.game.players:
				command.update_and_send(status='success', connection=player.connection)