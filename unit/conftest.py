import pytest
import types
import config
import random

@pytest.fixture
def get_args():
	def _get_args(stub, call_number, arg_number=None):
		if arg_number != None:
			return stub.call_args_list[call_number][0][arg_number]
		else:
			return stub.call_args_list[call_number][0]
	return _get_args

@pytest.fixture(autouse=True)
def patch_command(mocker):
	mocker.patch('src.common.command.send')
	mocker.patch('src.common.command.update_and_send')
	mocker.patch('src.common.command.update_and_send_to_all')
	mocker.patch('src.common.command.create_and_send')
	mocker.patch('src.common.command.create_and_send_to_all')

@pytest.fixture(autouse=True)
def seed_random():
	random.seed(0)

@pytest.fixture
def create_generic_state():
	def _create_generic_state(mocker):
		state = types.SimpleNamespace()
		methods = [
			'back', 
			'exit', 
			'game_full', 
			'invalid_game_name', 
			'invalid_player_name', 
			'name_too_long', 
			'name_too_short', 
			'next', 
			'not_enough_players',
			'set_available_characters',
			'set_character_selections',
			'set_current_player',
			'set_games',
			'set_players',
			'set_player_order',
			'set_player_positions'
		]
		for method in methods:
			setattr(state, method, mocker.stub())
		return state
	return _create_generic_state

@pytest.fixture
def create_game():
	def _create_game(mocker, player_count=0):
		game = types.SimpleNamespace()
		game.name = 'game name'
		game.players = []
		for i in range(player_count):
			player = types.SimpleNamespace()
			player.name = f'player{i}'
			player.connection = f'player{i}_connection'
			player.display_name = f'player{i}_display_name'
			player.set_position = mocker.stub()
			player.set_character = mocker.stub()
			game.players.append(player)
		game.set_state = mocker.stub()
		return game
	return _create_game
