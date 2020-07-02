from lattice2d.full.server import ServerCore as Lattice2dServerCore, ServerGame
from lattice2d.network import Server
from src.server.server_states import ServerLobbyState
from src.common.grid import Player

class ServerCore(Lattice2dServerCore):
	def create_player_handler(self, command):
		already_used = next(iter(p for p in self.players if p.name == command.data['player_name']), False)
		if len(command.data['player_name']) < 6:
			command.update_and_send(status='name_too_short')
		elif len(command.data['player_name']) > 25:
			command.update_and_send(status='name_too_long')
		elif already_used:
			command.update_and_send(status='invalid_name')
		else:
			self.players.append(Player(command.data['player_name'], command.connection))
			command.update_and_send(status='success')

	def create_game_handler(self, command):
		already_used = next(iter(g for g in self.children if g.name == command.data['game_name']), False)
		if len(command.data['game_name']) < 6:
			command.update_and_send(status='name_too_short')
		elif len(command.data['game_name']) > 40:
			command.update_and_send(status='name_too_long')
		elif already_used:
			command.update_and_send(status='invalid_name')
		else:
			game = ServerGame(command.data['game_name'], self.destroy_game)
			self.children.append(game)
			player = next(p for p in self.players if p.connection == command.connection)
			game.add_player(player, True)
			command.update_and_send(status='success')
