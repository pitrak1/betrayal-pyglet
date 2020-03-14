import pytest
from src.server.states import lobby_state as lobby_state_module
from src.server import player as player_module

@pytest.fixture
def make_lobby_state():
	def _make_lobby_state(mocker, player_count=0):
		mocker.patch('src.shared.command.create_and_send')
		mocker.patch('src.shared.command.update_and_send')
		data = {}

		data['players'] = []
		for index in range(player_count):
			player = player_module.Player(f'player {index}', False, f'player connection {index}')
			if index == 0: player.host = True
			data['players'].append(player)

		data['rooms'] = []
		data['name'] = 'game name'
		data['password'] = 'game password'

		return lobby_state_module.LobbyState(data, mocker.stub(), mocker.stub())
	return _make_lobby_state