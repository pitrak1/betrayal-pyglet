import random
import config
from lattice2d.full.server import ServerState
from lattice2d.grid import TileGrid, get_distance
from lattice2d.network import NetworkCommand
from lattice2d.utilities.threaded_sync import ThreadedSync
from lattice2d.nodes import Node
from src.server.server_grid import ServerRoomGrid
from src.common import constants

class GameState(ServerState):
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
