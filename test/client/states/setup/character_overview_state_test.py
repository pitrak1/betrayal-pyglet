import pytest
import pyglet
import sys
from src.client.states.setup import character_overview_state
from src.client.states.game import game_state
import config
from src.shared import constants
import types

class TestCharacterOverviewState():
	def test_adds_network_get_character_selections_on_creation(self, mocker, get_args):
		state = character_overview_state.CharacterOverviewState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_get_character_selections'

	def test_sets_waiting_text_if_current_player_on_confirm_characters(self, mocker, get_args):
		state = character_overview_state.CharacterOverviewState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		waiting_text = types.SimpleNamespace()
		waiting_text.text = ''
		state.elements = { 'waiting_text': waiting_text }
		state.confirm_characters()
		assert waiting_text.text == 'Waiting for other players...'

	def test_adds_network_confirm_character_selections_if_current_player_on_confirm_characters(self, mocker, get_args):
		state = character_overview_state.CharacterOverviewState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		waiting_text = types.SimpleNamespace()
		waiting_text.text = ''
		state.elements = { 'waiting_text': waiting_text }
		state.confirm_characters()
		assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_confirm_character_selections'

	def test_does_not_add_network_confirm_character_selections_if_not_current_player_on_confirm_characters(self, mocker):
		state = character_overview_state.CharacterOverviewState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		waiting_text = types.SimpleNamespace()
		waiting_text.text = ''
		state.elements = { 'waiting_text': waiting_text }
		state.confirm_characters()
		state.confirm_characters()
		assert state.add_command.call_count == 2

	def test_sets_state_to_game_state_on_next(self, mocker, get_args):
		state = character_overview_state.CharacterOverviewState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.next()
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), game_state.GameState)
