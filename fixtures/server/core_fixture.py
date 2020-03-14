import pytest
from src.server import core as core_module, game as game_module, player as player_module

@pytest.fixture
def make_core():
	def _make_core(mocker, player_count=0):
		mocker.patch('src.shared.command.update_and_send')
		core = core_module.Core()

		core.games['variable player game'] = game_module.Game('variable player game', 'variable player game password')
		for index in range(player_count):
			player = player_module.Player(f'variable player {index}', False, f'variable player connection {index}')
			core.games['variable player game'].players.append(player)
			player.game = core.games['variable player game']
			core.players.append(player)
		core.games['variable player game'].on_update = mocker.stub()

		core.games['fixed player game'] = game_module.Game('fixed player game', 'fixed player game password')
		for index in range(2):
			player = player_module.Player(f'fixed player {index}', False, f'fixed player connection {index}')
			core.games['fixed player game'].players.append(player)
			player.game = core.games['fixed player game']
			core.players.append(player)
		core.games['fixed player game'].on_update = mocker.stub()

		core.games['empty game'] = game_module.Game('empty game', 'empty game password')
		core.games['empty game'].on_update = mocker.stub()

		player = player_module.Player('free player', False, f'free player connection')
		core.players.append(player)

		core.on_command = mocker.stub()

		return core
	return _make_core