import pytest
import pyglet
import sys
from src.client.states.setup import character_selection_state, character_overview_state
import config
from src.shared import constants
import types

class TestCharacterSelectionState():
	def test_adds_network_get_available_characters_on_creation(self, mocker, get_args):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_get_available_characters'

	def test_decrements_character_index_on_go_left(self, mocker):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.character_index = 3
		state.go_left()
		assert state.character_index == 2

	def test_sets_character_index_to_max_if_negative_on_go_left(self, mocker):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.go_left()
		assert state.character_index == len(config.CHARACTERS) - 1

	def test_increment_character_index_on_go_right(self, mocker):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.character_index = 3
		state.go_right()
		assert state.character_index == 4

	def test_sets_character_index_to_zero_if_past_count_on_go_right(self, mocker):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.character_index = len(config.CHARACTERS) - 1
		state.go_right()
		assert state.character_index == 0

	def test_sets_available_characters_on_set_available_character(self, mocker):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		characters = ['character1', 'character2', 'character3']
		state.set_available_characters(characters)
		assert state.available_characters == characters

	def test_adds_network_get_current_player_on_set_available_character(self, mocker, get_args):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		characters = ['character1', 'character2', 'character3']
		state.set_available_characters(characters)
		assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_get_current_player'

	def test_sets_title_and_current_player_on_set_current_player(self, mocker):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.set_current_player('some_player')
		assert state.current_player == False
		assert state.title == 'some_player is choosing'

	def test_sets_title_and_current_player_when_self_on_set_current_player(self, mocker):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.set_current_player('self')
		assert state.current_player == True
		assert state.title == 'You are choosing'

	def test_adds_network_select_character_if_current_player_on_select_character(self, mocker, get_args):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.current_player = True
		state.select_character()
		assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_select_character'

	def test_does_not_add_network_select_character_if_not_current_player_on_select_character(self, mocker):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.current_player = False
		state.select_character()
		assert state.add_command.call_count == 1

	def test_sets_state_to_character_overview_state_on_next(self, mocker, get_args):
		state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.next()
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), character_overview_state.CharacterOverviewState)
