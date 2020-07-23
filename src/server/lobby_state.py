from lattice2d.server.server_state import ServerState
from constants import MINIMUM_PLAYERS

class LobbyState(ServerState):
	def network_start_game_handler(self, command):
		if len(self.game.players) < MINIMUM_PLAYERS:
			command.update_and_send(status='not_enough_players')
		else:
			self.to_setup_state()
			for player in self.game.players:
				command.update_and_send(status='success', connection=player.connection)