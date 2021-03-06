import random
from lattice2d.server import ServerState
from lattice2d.grid import TileGrid, get_distance
from lattice2d.command import Command
from lattice2d.utilities import ThreadedSync
from lattice2d.nodes import Node
from src.common.grid import RoomGrid
from constants import Constants

class LobbyState(ServerState):
	def start_game_handler(self, command):
		if len(self.state_machine.players) < Constants.min_players_per_game:
			command.update_and_send(status='not_enough_players')
		else:
			self.to_setup_state()
			for player in self.state_machine.players:
				command.update_and_send(status='success', connection=player.connection)

class SetupState(ServerState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		random.shuffle(self.state_machine.players)
		self.waiting = ThreadedSync(len(self.state_machine.players))
		self.state_machine.current_player_index = len(self.state_machine.players) - 1
		self.characters = []
		for character in Constants.characters:
			self.characters.append(character['key'])

	def get_player_order_handler(self, command):
		parsed_players = [player.name for player in self.state_machine.players]
		command.update_and_send(status='success', data={ 'players': parsed_players })

	def confirm_player_order_handler(self, command):
		self.waiting.count()
		if self.waiting.done():
			for player in self.state_machine.players:
				command.update_and_send(status='success', connection=player.connection)

	def get_available_characters_handler(self, command):
		command.update_and_send(status='success', data={ 'characters': self.characters })

	def select_character_handler(self, command):
		if self.state_machine.is_current_player(command):
			current_player = self.state_machine.get_current_player()
			character_entry = next(character for character in Constants.characters if character['key'] == command.data['character'])
			current_player.set_character(character_entry)
			self.characters = [x for x in self.characters if x != character_entry['key'] and x not in character_entry['related']]

			self.state_machine.current_player_index -= 1
			current_player = self.state_machine.get_current_player()
			if self.state_machine.current_player_index < 0:
				for player in self.state_machine.players:
					Command.create_and_send('all_characters_selected', {}, 'success', player.connection)
			else:
				for player in self.state_machine.players:
					Command.create_and_send('get_available_characters', { 'characters': self.characters }, 'success', player.connection)

	def get_character_selections_handler(self, command):
		selections = [(p.name, p.entry['display_name']) for p in self.state_machine.players]
		command.update_and_send(status='success', data={ 'selections': selections })

	def confirm_character_selections_handler(self, command):
		self.waiting.count()
		if self.waiting.done():
			self.to_game_state()
			for player in self.state_machine.players:
				command.update_and_send(status='success', connection=player.connection)

class GameState(ServerState):
	def __init__(self, state_machine, custom_data={}):
		super().__init__(state_machine, custom_data)
		self.state_machine.current_player_index = 0
		self.rooms = RoomGrid(state_machine, Constants.grid_dimensions)
		self.children = [self.rooms]

	def network_get_player_positions_handler(self, command):
		parsed_players = [(player.name, player.character_entry['variable_name'], player.grid_position) for player in self.state_machine.players]
		command.update_and_send(status='success', data={ 'players': parsed_players })

	def network_get_current_player_handler(self, command):
		current_player = self.state_machine.get_current_player().name
		command.update_and_send(status='success', data={ 'player_name': current_player })

	def network_move_handler(self, command):
		player = next(p for p in self.state_machine.players if p.name == command.data['player'])
		assert player and self.state_machine.is_current_player(player)
		assert get_distance(player.grid_position, command.data['grid_position']) == 1
		self.rooms.move_actor(command.data['grid_position'], player)
		command.update_and_send(status='success')