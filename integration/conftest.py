import pytest
import types
from config import CONFIG
from lattice2d.config import Config
from lattice2d.states import StateMachine
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
    def _get_keyword_args(stub, call_number, key=None):
        if key != None:
            return stub.call_args_list[call_number][1][key]
        else:
            return stub.call_args_list[call_number][1]
    return _get_keyword_args
