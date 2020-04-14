import pytest
import pyglet
import sys
from src.client.setup import character_selection_state, character_overview_state
import config
from src.common import constants
import types

class TestCharacterSelectionState():
	class TestConstructor():
		def test_adds_network_get_available_characters(self, mocker, get_args):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_get_available_characters'

	class TestGoLeft():
		def test_decrements_character_index(self, mocker):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.character_index = 3
			state.go_left()
			assert state.character_index == 2

		def test_sets_character_index_to_max_if_negative(self, mocker):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.go_left()
			assert state.character_index == len(config.CHARACTERS) - 1

	class TestGoRight():
		def test_increment_character_index(self, mocker):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.character_index = 3
			state.go_right()
			assert state.character_index == 4

		def test_sets_character_index_to_zero_if_past_count(self, mocker):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.character_index = len(config.CHARACTERS) - 1
			state.go_right()
			assert state.character_index == 0

	class TestSetAvailableCharacters():
		def test_sets_available_characters(self, mocker):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			characters = ['character1', 'character2', 'character3']
			state.set_available_characters(characters)
			assert state.available_characters == characters

		def test_adds_network_get_current_player(self, mocker, get_args):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			characters = ['character1', 'character2', 'character3']
			state.set_available_characters(characters)
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_get_current_player'

	class TestSetCurrentPlayer():
		def test_sets_title_and_current_player(self, mocker):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.set_current_player('some_player')
			assert state.current_player == False
			assert state.title == 'some_player is choosing'

		def test_sets_title_and_current_player_when_self(self, mocker):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.set_current_player('self')
			assert state.current_player == True
			assert state.title == 'You are choosing'

	class TestSelectCharacter():
		def test_adds_network_select_character_if_current_player(self, mocker, get_args):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.current_player = True
			state.select_character()
			assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_select_character'

		def test_does_not_add_network_select_character_if_not_current_player(self, mocker):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.current_player = False
			state.select_character()
			assert state.add_command.call_count == 1

	class TestNext():
		def test_sets_state_to_character_overview_state(self, mocker, get_args):
			state = character_selection_state.CharacterSelectionState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
			state.next()
			assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), character_overview_state.CharacterOverviewState)
