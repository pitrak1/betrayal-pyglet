import pytest
import types
import config

@pytest.fixture
def get_args():
	def _get_args(stub, call_number, argument_number=None):
		if argument_number != None:
			return stub.call_args_list[call_number][0][argument_number]
		else:
			return stub.call_args_list[call_number][0]
	return _get_args

