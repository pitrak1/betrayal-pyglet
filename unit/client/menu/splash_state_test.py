import pytest
import pyglet
from src.client.menu import splash_state, create_player_state
import config

class TestSplashState():
	class TestBegin():
		def test_sets_state_to_create_player_state(self, mocker, get_args):
			state = splash_state.SplashState({}, mocker.stub(), mocker.stub(), testing=True)
			state.begin()
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), create_player_state.CreatePlayerState)
