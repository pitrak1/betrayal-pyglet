from lattice2d.server import ServerState
from constants import MINIMUM_PLAYERS

class LobbyState(ServerState):
	def network_start_game_handler(self, command):
		if len(self.state_machine.get_players()) < MINIMUM_PLAYERS:
			command.update_and_send(status='not_enough_players')
		else:
			self.to_setup_state()
			for player in self.state_machine.get_players():
				command.update_and_send(status='success', connection=player.connection)