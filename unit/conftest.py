import pytest
import types
import config
import random
from lattice2d.config import Config
from lattice2d.full.full_server import FullServerGame

@pytest.fixture
def get_args():
	def _get_args(stub, call_number, arg_number=None):
		if arg_number != None:
			return stub.call_args_list[call_number][0][arg_number]
		else:
			return stub.call_args_list[call_number][0]
	return _get_args


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

@pytest.fixture(autouse=True)
def load_config():
	config = Config(TEST_CONFIG)
