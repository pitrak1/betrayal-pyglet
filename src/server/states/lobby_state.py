from src.server.states import state, character_selection_state
from src.shared import command as command_module

class LobbyState(state.State):
	def __init__(self, data, set_state, add_command):
		super().__init__(data, set_state, add_command)
		self.name = data['name']
		self.password = data['password']

	def network_get_players_in_game_handler(self, command, state=None):
		self.__send_players_in_game(command.data['exception'])

	def server_broadcast_players_handler(self, command, state=None):
		self.__send_players_in_game(command.data['exception'])

	def network_start_game_handler(self, command, state=None):
		player = next(p for p in self.players if command.data['connection'] == p)
		if player.host:
			self.set_state(character_selection_state.CharacterSelectionState(
				{ 'players': self.players, 'rooms': self.rooms }, 
				self.set_state, 
				self.add_command
			))
			for game_player in self.players:
				command_module.update_and_send(command, { 'status': 'success', 'connection': game_player.connection })
		else:
			command_module.update_and_send(command, { 'status': 'not_host' })

	def network_leave_game_handler(self, command, state=None):
		player = next(p for p in self.players if command.data['connection'] == p)
		player.game = None
		self.players.remove(player)
		command_module.update_and_send(command, { 'status': 'success' })
		if self.players:
			self.__send_players_in_game(None)
		else:
			self.add_command(command_module.Command('server_destroy_game', { 'game_name': self.name }))

	def __send_players_in_game(self, exception):
		parsed_players = [(p.name, p.host) for p in self.players]
		for player in self.players:
			if player != exception:
				command_module.create_and_send(
					'network_get_players_in_game',
					{ 'status': 'success', 'players': parsed_players, 'connection': player.connection }
				)
