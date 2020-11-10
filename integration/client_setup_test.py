import pytest
import pyglet
from integration import helpers
from src.client.setup_states import PlayerOrderState, CharacterSelectionState, CharacterOverviewState
from src.client.game_states import BaseState
from lattice2d.command import Command
from constants import Constants
import sys

client = None

@pytest.fixture(autouse=True)
def setup():
	global client
	client = helpers.create_client()

class TestSetup():
	class TestPlayerOrder():
		class TestPlayerOrderResponse():
			def test_sets_player_order_text_if_get_player_order_success(self):
				helpers.to_player_order_state(client)
				helpers.add_command(client, Command('get_player_order', { 'players': ['player1', 'player2', 'player3'] }, 'success'))
				assert helpers.text(client, 'player_order_text') == 'player1, player2, player3'

			def test_does_not_set_player_order_text_if_get_player_order_error(self):
				helpers.to_player_order_state(client)
				helpers.add_command(client, Command('get_player_order', { 'players': ['player1', 'player2', 'player3'] }, 'error'))
				assert helpers.text(client, 'player_order_text') == ''

		class TestContinue():
			def test_sends_command_when_continue_is_clicked(self, mocker):
				helpers.to_player_order_state(client)
				helpers.assert_sends_command_of_type(mocker, client, lambda: helpers.click_button(client, 'continue_button'), 'confirm_player_order')

			def test_does_not_send_multiple_commands(self, mocker):
				helpers.to_player_order_state(client)
				mocker.patch.object(client.current_state, 'add_command')
				helpers.click_button(client, 'continue_button')
				helpers.click_button(client, 'continue_button')
				assert client.current_state.add_command.call_count == 1

		class TestConfirmPlayerOrder():
			def test_transitions_if_confirm_player_order_success(self):
				helpers.to_player_order_state(client)
				helpers.add_command(client, Command('confirm_player_order', {}, 'success'))
				assert helpers.is_state(client, CharacterSelectionState)

			def test_does_not_transition_if_confirm_player_order_error(self):
				helpers.to_player_order_state(client)
				helpers.add_command(client, Command('confirm_player_order', {}, 'error'))
				assert helpers.is_state(client, PlayerOrderState)

	class TestCharacterSelection():
		class TestGetAvailableCharactersResponse():
			def test_sends_command_when_get_available_characters_success(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.assert_sends_command_of_type(mocker, client, lambda: helpers.add_command(client, Command('get_available_characters', { 'characters': ['character1', 'character2'] }, 'success')), 'get_current_player')

			def test_does_not_send_command_when_get_available_characters_error(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.assert_does_not_send_command(client, lambda: helpers.add_command(client, Command('get_available_characters', { 'characters': ['character1', 'character2'] }, 'error')))

		class TestGetCurrentPlayerResponse():
			def test_adds_select_button_if_current_player(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'self' }, 'success'))
				helpers.assert_has_components(client, 'select_button')

			def test_does_not_add_select_button_if_current_player_with_error(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'self' }, 'error'))
				helpers.assert_does_not_have_components(client, 'select_button')

			def test_removes_select_button_if_not_current_player(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'self' }, 'success'))
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'player1' }, 'success'))
				helpers.assert_does_not_have_components(client, 'select_button')

			def test_does_not_remove_select_button_if_not_current_player_with_error(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'self' }, 'success'))
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'player1' }, 'error'))
				helpers.assert_has_components(client, 'select_button')

		class TestCharacterTiles():
			def test_starts_on_first_character(self, mocker):
				helpers.to_character_selection_state(client)
				client.current_state.redraw_tile()
				helpers.assert_character_tile(client, 0)

			def test_moves_left(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.click_button(client, 'left_button')
				helpers.assert_character_tile(client, len(Constants.characters) - 1)

			def test_moves_right(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.click_button(client, 'right_button')
				helpers.assert_character_tile(client, 1)

			def test_characters_available_are_active(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_available_characters', { 'characters': [Constants.characters[0]['key']] }, 'success'))
				client.current_state.redraw_tile()
				assert helpers.get_character_tile(client).active

			def test_characters_not_available_are_not_active(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_available_characters', { 'characters': [] }, 'success'))
				client.current_state.redraw_tile()
				assert not helpers.get_character_tile(client).active

		class TestSelecting():
			def test_does_not_send_command_if_not_current_player(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_available_characters', { 'characters': [Constants.characters[0]['key']] }, 'success'))
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'player2' }, 'success'))
				helpers.assert_does_not_send_command(client, lambda: client.current_state.select_character())

			def test_does_not_send_command_if_character_not_available(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_available_characters', { 'characters': [] }, 'success'))
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'self' }, 'success'))
				helpers.assert_does_not_send_command(client, lambda: helpers.click_button(client, 'select_button'))

			def test_sends_command_if_character_available_and_current_player(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('get_available_characters', { 'characters': [Constants.characters[0]['key']] }, 'success'))
				helpers.add_command(client, Command('get_current_player', { 'player_name': 'self' }, 'success'))
				helpers.assert_sends_command_of_type(mocker, client, lambda: helpers.click_button(client, 'select_button'), 'select_character')

		class TestAllCharactersSelectedResponse():
			def test_transitions_if_success(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('all_characters_selected', {}, 'success'))
				assert helpers.is_state(client, CharacterOverviewState)

			def test_does_not_transition_if_error(self, mocker):
				helpers.to_character_selection_state(client)
				helpers.add_command(client, Command('all_characters_selected', {}, 'error'))
				assert helpers.is_state(client, CharacterSelectionState)
	class TestCharacterOverviewState():
		class TestGetCharacterSelectionsResponse():
			def test_displays_character_selections_on_success(self, mocker):
				helpers.to_character_overview_state(client)
				helpers.add_command(client, Command('get_character_selections', { 'selections': [('player1', 'Character 1'), ('player2', 'Character 2')] }, 'success'))
				assert client.current_state.selections_text.get_text() == 'player1: Character 1\nplayer2: Character 2\n'

			def test_does_not_display_character_selections_on_error(self, mocker):
				helpers.to_character_overview_state(client)
				helpers.add_command(client, Command('get_character_selections', { 'selections': [('player1', 'Character 1'), ('player2', 'Character 2')] }, 'error'))
				assert client.current_state.selections_text.get_text() == ''

		class TestConfirmCharacters():
			def test_sends_command_when_continue_is_clicked(self, mocker):
				helpers.to_character_overview_state(client)
				helpers.assert_sends_command_of_type(mocker, client, lambda: helpers.click_button(client, 'confirm_button'), 'confirm_character_selections')

			def test_does_not_send_multiple_commands(self, mocker):
				helpers.to_character_overview_state(client)
				mocker.patch.object(client.current_state, 'add_command')
				helpers.click_button(client, 'confirm_button')
				helpers.click_button(client, 'confirm_button')
				assert client.current_state.add_command.call_count == 1

		class TestConfirmCharacterSelectionsResponse():
			def test_transitions_if_success(self, mocker):
				helpers.to_character_overview_state(client)
				helpers.add_command(client, Command('confirm_character_selections', {}, 'success'))
				assert helpers.is_state(client, BaseState)

			def test_does_not_transition_if_error(self, mocker):
				helpers.to_character_overview_state(client)
				helpers.add_command(client, Command('confirm_character_selections', {}, 'error'))
				assert helpers.is_state(client, CharacterOverviewState)
