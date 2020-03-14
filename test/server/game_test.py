import pytest
import pyglet
from src.server import game as game_module
from src.server.states import lobby_state

@pytest.mark.usefixtures('make_node')
class TestGame():
	def test_starts_in_lobby_state(self):
		game = game_module.Game('name', 'password')
		assert isinstance(game.current_state, lobby_state.LobbyState)

	def test_allows_setting_current_state(self):
		game = game_module.Game('name', 'password')
		game.set_state('some_state')
		assert game.current_state == 'some_state'

	def test_allows_adding_commands_that_are_sent_to_state_on_update(self, mocker, make_node):
		game = game_module.Game('name', 'password')
		game.set_state(make_node(mocker))
		game.add_command('some_command')
		game.current_state.on_command.assert_not_called()
		game.on_update()
		game.current_state.on_command.assert_called_once_with('some_command')
