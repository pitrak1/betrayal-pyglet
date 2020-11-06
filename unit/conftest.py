import pytest
import types
import config
import random

@pytest.fixture
def get_positional_args():
	def _get_positional_args(stub, call_number, arg_number=None):
		if arg_number != None:
			return stub.call_args_list[call_number][0][arg_number]
		else:
			return stub.call_args_list[call_number][0]
	return _get_positional_args

@pytest.fixture
def get_keyword_args():
    def _get_keyword__args(stub, call_number, key=None):
        if key != None:
            return stub.call_args_list[call_number][1][key]
        else:
            return stub.call_args_list[call_number][1]
    return _get_keyword_args

@pytest.fixture(autouse=True)
def seed_random():
	random.seed(0)

TEST_CONFIG = {
    'command_types': [
        'network_start_game',
        'network_get_player_order',
        'network_confirm_player_order',
        'network_get_available_characters',
        'network_select_character',
        'network_all_characters_selected',
        'network_get_character_selections',
        'network_confirm_character_selections'
    ],
    'full_solution': {}
}

# @pytest.fixture(autouse=True)
# def load_config():
# 	config = Config(TEST_CONFIG)
