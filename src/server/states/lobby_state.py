from src.server.states import character_selection_state, state
from src.common import command, logger

class LobbyState(state.State):
	def network_start_game_handler(self, command_, state=None):
		logger.log(f'Lobby State {self.game.name} handling command', logger.LOG_LEVEL_COMMAND)
		if len(self.game.players) < 2:
			command.update_and_send(command_, { 'status': 'not_enough_players' })
		else:
			self.game.set_state(character_selection_state.CharacterSelectionState(self.game))
			command.update_and_send_to_all(command_, { 'status': 'success' }, self.game.players)
