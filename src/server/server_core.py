from lattice2d.full.full_server import FullServer, FullServerGame, FullServerGameList
from lattice2d.network import Server
from src.server.server_states import ServerLobbyState
from src.common.grid import Player

class ServerGame(FullServerGame):
	def __init__(self, name, destroy_game):
		super().__init__(name, destroy_game)
		self.set_state(ServerLobbyState(self))

class ServerCore(FullServer):
	def __init__(self):
		super().__init__()
		self.server = Server(self.add_command)

	def create_player_handler(self, command):
		if len(command.data['player_name']) < 6:
			command.update_and_send(status='name_too_short')
		elif len(command.data['player_name']) > 25:
			command.update_and_send(status='name_too_long')
		elif self.players.find_by_name(command.data['player_name']):
			command.update_and_send(status='invalid_name')
		else:
			self.players.append(Player(command.data['player_name'], command.connection))
			command.update_and_send(status='success')

	def create_game_handler(self, command):
		if len(command.data['game_name']) < 6:
			command.update_and_send(status='name_too_short')
		elif len(command.data['game_name']) > 40:
			command.update_and_send(status='name_too_long')
		elif self.children.find_by_name(command.data['game_name']):
			command.update_and_send(status='invalid_name')
		else:
			game = ServerGame(command.data['game_name'], self.children.destroy)
			self.children.append(game)
			game.add_player(self.players.find_by_connection(command.connection), True)
			command.update_and_send(status='success')
