from src.client.states.menu import main_menu_state
from src.shared import command
import random
import time

def click_button(game_, element_key):
	game_.current_state.elements[element_key].on_click()
	game_.on_update(0.1)

def is_state(game_, state_class):
	return isinstance(game_.current_state, state_class)

def enter_text(game_, element_key, text):
	command_ = command.Command('client_text_entered', { 'text': text })
	game_.current_state.elements[element_key].selected = True
	game_.current_state.elements[element_key].client_text_entered_handler(command_, None)
	game_.on_update(0.1)

def get_text(game_, element_key):
	return game_.current_state.elements[element_key].get_text()

def wait_for_state(game_, state_class):
	start = time.perf_counter()
	while not is_state(game_, state_class):
		game_.on_update(0.1)
		current = time.perf_counter()
		if (current - start) > 5:
			raise RuntimeError(f'timeout waiting for {state_class.__name__}')

def to_menu_create_player_state(game_):
	click_button(game_, 'begin_button')

def to_menu_main_menu_state(game_):
	to_menu_create_player_state(game_)
	player_name = f'player{random.randrange(1000)}'
	enter_text(game_, 'player_name_input', player_name)
	click_button(game_, 'continue_button')
	wait_for_state(game_, main_menu_state.MainMenuState)
	return player_name

def to_menu_create_game_state(game_):
	player_name = to_menu_main_menu_state(game_)
	click_button(game_, 'create_button')
	return player_name

def to_menu_game_list_state(game_):
	player_name = to_menu_main_menu_state(game_)
	click_button(game_, 'join_button')
	return player_name
