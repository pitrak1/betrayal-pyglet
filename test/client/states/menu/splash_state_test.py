import pytest
import pyglet
from src.client.states.menu import splash_state as splash_state_module, create_player_state as create_player_state_module
from src.shared import command as command_module

class TestSplashState():
	class TestBegin():
		def test_sets_state_to_create_player_state(self, mocker, make_asset_manager, get_args):
			mocker.patch('pyglet.sprite')
			state = splash_state_module.SplashState({ 'assets': make_asset_manager(mocker) }, mocker.stub(), mocker.stub())
			state.begin()
			state.set_state.assert_called_once()
			assert isinstance(get_args(state.set_state, 0, 0), create_player_state_module.CreatePlayerState)
