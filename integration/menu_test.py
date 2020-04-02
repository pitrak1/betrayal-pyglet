import pytest
import pyglet
from src.client import game
from src.client.states.menu import splash_state, create_player_state, main_menu_state, create_game_state, game_list_state
from integration import helpers
import config

class TestMenu():
	def test_transitions_to_create_player_state(self):
		game_ = game.Game()
		helpers.to_menu_create_player_state(game_)
		assert helpers.is_state(game_, create_player_state.CreatePlayerState)

	def test_does_not_transition_to_main_menu_state_if_player_name_is_too_short(self):
		game_ = game.Game()
		helpers.to_menu_create_player_state(game_)
		helpers.enter_text(game_, 'player_name_input', '12345')
		helpers.click_button(game_, 'continue_button')
		assert helpers.is_state(game_, create_player_state.CreatePlayerState)

	def test_truncates_player_name_if_player_name_is_too_long(self):
		game_ = game.Game()
		helpers.to_menu_create_player_state(game_)
		helpers.enter_text(game_, 'player_name_input', '123456789012345678901234567890')
		assert len(helpers.get_text(game_, 'player_name_input')) == 25

	def test_transitions_to_main_menu_state(self):
		game_ = game.Game()
		helpers.to_menu_main_menu_state(game_)
		assert helpers.is_state(game_, main_menu_state.MainMenuState)

	def test_transitions_to_create_game_state(self):
		game_ = game.Game()
		helpers.to_menu_create_game_state(game_)
		assert helpers.is_state(game_, create_game_state.CreateGameState)

	def test_transitions_to_game_list_state(self):
		game_ = game.Game()
		helpers.to_menu_game_list_state(game_)
		assert helpers.is_state(game_, game_list_state.GameListState)