from src.client.menu_states import MainMenuState, LobbyState
from lattice2d.command import Command
import random
import time
from config import CONFIG
from lattice2d.config import Config
from lattice2d.states import StateMachine

def create_client():
    Config(CONFIG)
    return StateMachine(Config()['client_states'])

def click_button(state_machine, component_key):
	state_machine.current_state.get_component(component_key).on_click()
	state_machine.on_update(0.1)

def add_command(state_machine, command):
	state_machine.add_command(command)
	state_machine.on_update(0.1)

def is_state(state_machine, state_class):
	return isinstance(state_machine.current_state, state_class)

def enter_text(state_machine, component_key, text):
	state_machine.add_command(Command('text', { 'text': text }))
	state_machine.current_state.get_component(component_key).selected = True
	state_machine.on_update(0.1)

def get_text(state_machine, component_key):
	return state_machine.current_state.get_component(component_key).get_text()

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



