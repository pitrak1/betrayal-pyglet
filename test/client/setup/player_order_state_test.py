import pytest
import pyglet
import sys
from src.client.setup import player_order_state, character_selection_state
import config
from src.shared import constants
import types

class TestPlayerOrderState():
	def test_adds_network_get_player_order_on_creation(self, mocker, get_args):
		state = player_order_state.PlayerOrderState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		assert get_args(state.add_command, call_number=0, arg_number=0).type == 'network_get_player_order'

	def test_sets_waiting_text_on_continue_click(self, mocker, get_args):	
		state = player_order_state.PlayerOrderState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		waiting_text = types.SimpleNamespace()
		waiting_text.text = ''
		state.elements = { 'waiting_text': waiting_text }
		state.continue_()
		assert waiting_text.text == 'Waiting for other players...'

	def test_adds_network_confirm_player_order_on_continue_click(self, mocker, get_args):	
		state = player_order_state.PlayerOrderState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		waiting_text = types.SimpleNamespace()
		waiting_text.text = ''
		state.elements = { 'waiting_text': waiting_text }
		state.continue_()
		assert get_args(state.add_command, call_number=1, arg_number=0).type == 'network_confirm_player_order'

	def test_does_not_add_network_confirm_player_order_on_continue_click_after_first(self, mocker, get_args):	
		state = player_order_state.PlayerOrderState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		waiting_text = types.SimpleNamespace()
		waiting_text.text = ''
		state.elements = { 'waiting_text': waiting_text }
		state.continue_()
		state.continue_()
		assert state.add_command.call_count == 2

	def test_sets_state_to_character_selection_state_on_next(self, mocker, get_args):
		state = player_order_state.PlayerOrderState({}, mocker.stub(), mocker.stub(), 'player_name', 'game_name', True, testing=True)
		state.next()
		assert isinstance(get_args(stub=state.set_state, call_number=0, arg_number=0), character_selection_state.CharacterSelectionState)
