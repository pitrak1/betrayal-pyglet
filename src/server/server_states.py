import random
import config
from lattice2d.full.server import ServerState
from lattice2d.grid import TileGrid, get_distance
from lattice2d.network import NetworkCommand
from lattice2d.utilities.threaded_sync import ThreadedSync
from lattice2d.nodes import Node
from src.server.server_grid import ServerRoomGrid
from src.common import constants

class ServerLobbyState(ServerState):
	def network_start_game_handler(self, command):
		if len(self.game.players) < constants.MINIMUM_PLAYERS:
			command.update_and_send(status='not_enough_players')
		else:
			self.to_setup_state()
			for player in self.game.players:
				command.update_and_send(status='success', connection=player.connection)

class ServerSetupState(ServerState):
	def __init__(self, game, custom_data={}):
		super().__init__(game, custom_data)
		random.shuffle(self.game.players)
		self.waiting = ThreadedSync(len(self.game.players))
		self.game.current_player_index = len(self.game.players) - 1
		self.characters = []
		for character in config.CHARACTERS:
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
			character_entry = next(character for character in config.CHARACTERS if character['variable_name'] == command.data['character'])
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
		selections = [(p.name, p.display_name) for p in self.game.players]
		command.update_and_send(status='success', data={ 'selections': selections })

	def network_confirm_character_selections_handler(self, command):
		self.waiting.count()
		if self.waiting.done():
			print('game')
			# self.game.set_state(ServerGameState(self.game))
			# for player in self.game.players:
			# 	command.update_and_send(status='success', connection=player.connection)

class ServerGameState(ServerState):
	def __init__(self, game):
		super().__init__(game)
		self.game.current_player_index = 0
		self.rooms = ServerRoomGrid()
		self.children = [self.rooms]
		for player in self.game.players:
			self.rooms.add_actor((0, 0), player)

	def network_get_player_positions_handler(self, command):
		parsed_players = [(player.name, player.variable_name, player.grid_position) for player in self.game.players]
		command.update_and_send(status='success', data={ 'players': parsed_players })

	def network_get_current_player_handler(self, command):
		current_player = self.game.get_current_player().name
		command.update_and_send(status='success', data={ 'player_name': current_player })

	def network_move_handler(self, command):
		player = self.game.players.find_by_name(command.data['player'])
		assert player and self.game.is_current_player(player)
		assert get_distance(player.grid_position, command.data['grid_position']) == 1
		self.rooms.move_actor(command.data['grid_position'], player)
		command.update_and_send(status='success')

