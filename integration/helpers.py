import pytest
from src.client.menu_states import MainMenuState, LobbyState
from lattice2d.command import Command
import random
import time
from config import CONFIG
from constants import Constants
from lattice2d.config import Config
from lattice2d.states import StateMachine
from lattice2d.server import ServerGame, Player

def create_client():
    Config(CONFIG)
    return StateMachine(Config()['client_states'])

def create_game(mocker, number_of_players=0):
	Config(CONFIG)
	game_name = f'lobby{random.randrange(1000)}'
	game = ServerGame(game_name, mocker.stub())
	for i in range(number_of_players):
		game.players.append(Player(f'player{random.randrange(1000)}', game=game))
	return game

def assert_does_not_send_command(state_machine, callback):
	callback()
	assert not state_machine.command_queue.has_elements()

def assert_sends_command_of_type(mocker, state_machine, callback, command_type):
	mocker.patch.object(state_machine.current_state, 'add_command')
	callback()
	command = state_machine.current_state.add_command.call_args_list[0][0][0]
	assert command.type == command_type

def assert_has_components(state_machine, components):
	if isinstance(components, list):
		for component in components:
			assert state_machine.current_state.get_component(component)
	else:
		assert state_machine.current_state.get_component(components)

def assert_does_not_have_components(state_machine, components):
	if isinstance(components, list):
		for component in components:
			with pytest.raises(AssertionError):
				state_machine.current_state.get_component(component)
	else:
		with pytest.raises(AssertionError):
			state_machine.current_state.get_component(components)

def click_button(state_machine, component_key):
	state_machine.current_state.get_component(component_key).on_click()
	state_machine.on_update(0.1)

def add_command(state_machine, command):
	state_machine.add_command(command)
	state_machine.on_update(0.1)

def add_stubbed_command(mocker, state_machine, command):
	mocker.patch.object(command, 'update_and_send')
	state_machine.add_command(command)
	state_machine.on_update(0.1)

def is_state(state_machine, state_class):
	return isinstance(state_machine.current_state, state_class)

def enter_text(state_machine, component_key, text):
	state_machine.add_command(Command('text', { 'text': text }))
	state_machine.current_state.get_component(component_key).selected = True
	state_machine.on_update(0.1)

def text(state_machine, component_key):
	return state_machine.current_state.get_component(component_key).text

def get_text(state_machine, component_key):
	return state_machine.current_state.get_component(component_key).get_text()

def assert_character_tile(state_machine, character_index):
	assert state_machine.current_state.get_component('character_tile').display_name == Constants.characters[character_index]['display_name']

def get_character_tile(state_machine):
	return state_machine.current_state.get_component('character_tile')

def wait_for_state(state_machine, state_class):
	start = time.perf_counter()
	while not is_state(state_machine, state_class):
		state_machine.on_update(0.1)
		current = time.perf_counter()
		if (current - start) > 5:
			raise RuntimeError(f'timeout waiting for {state_class.__name__}')

def to_menu_create_player_state(state_machine):
	click_button(state_machine, 'begin_button')

def to_menu_main_menu_state(state_machine):
	to_menu_create_player_state(state_machine)
	player_name = f'player{random.randrange(1000)}'
	add_command(state_machine, Command('create_player', { 'player_name': player_name }, 'success'))
	wait_for_state(state_machine, MainMenuState)
	return player_name

def to_menu_create_game_state(state_machine):
	player_name = to_menu_main_menu_state(state_machine)
	click_button(state_machine, 'create_button')
	return player_name

def to_lobby_state_as_host(state_machine):
	player_name = to_menu_create_game_state(state_machine)
	game_name = f'lobby{random.randrange(1000)}'
	add_command(state_machine, Command('create_game', { 'game_name': game_name }, 'success'))
	wait_for_state(state_machine, LobbyState)
	return [player_name, game_name]

def to_menu_game_list_state(state_machine):
	player_name = to_menu_main_menu_state(state_machine)
	click_button(state_machine, 'join_button')
	return player_name

def to_lobby_state_as_player(state_machine):
	player_name = to_menu_game_list_state(state_machine)
	game_name = f'lobby{random.randrange(1000)}'
	add_command(state_machine, Command('join_game', { 'game_name': game_name }, 'success'))
	wait_for_state(state_machine, LobbyState)
	return [player_name, game_name]

def to_player_order_state(state_machine):
	[player_name, game_name] = to_lobby_state_as_host(state_machine)
	add_command(state_machine, Command('start_game', {}, 'success'))
	return [player_name, game_name]

def to_character_selection_state(state_machine):
	[player_name, game_name] = to_player_order_state(state_machine)
	add_command(state_machine, Command('confirm_player_order', {}, 'success'))
	return [player_name, game_name]

def to_character_overview_state(state_machine):
	[player_name, game_name] = to_character_selection_state(state_machine)
	add_command(state_machine, Command('all_characters_selected', {}, 'success'))
	return [player_name, game_name]



