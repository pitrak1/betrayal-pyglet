import random
import pytest
from src.server.states import character_selection_state as character_selection_state_module
from src.server import player as player_module

@pytest.fixture
def make_character_selection_state():
	def _make_character_selection_state(mocker, player_count=0):
		random.seed(0)
		mocker.patch('src.shared.command.create_and_send')
		mocker.patch('src.shared.command.update_and_send')
		data = {}

		data['players'] = []
		for index in range(player_count):
			player = player_module.Player(f'player {index}', False, f'player connection {index}')
			if index == 0: player.host = True
			data['players'].append(player)

		data['rooms'] = []

		return character_selection_state_module.CharacterSelectionState(data, mocker.stub(), mocker.stub())
	return _make_character_selection_state