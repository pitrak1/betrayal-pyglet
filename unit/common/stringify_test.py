import pytest
import pyglet
from src.common import stringify, command as command_module

class TestStringify():
	class TestStringify():
		def test_includes_type_as_first_value(self):
			command = command_module.Command('some_command_type', {})
			assert stringify.stringify(command) == 'some_command_type*'.encode()

		def test_allows_for_strings(self):
			command = command_module.Command('some_command_type', { 'some_key': 'some_value' })
			assert stringify.stringify(command) == 'some_command_type;some_key=some_value*'.encode()

		def test_allows_for_lists_of_strings(self):
			command = command_module.Command('some_command_type', { 'some_key': ['some_value_1', 'some_value_2'] })
			assert stringify.stringify(command) == 'some_command_type;some_key=[some_value_1|some_value_2]*'.encode()

		def test_allows_for_lists_of_tuples(self):
			command = command_module.Command('some_command_type', { 'some_key': [('tuple_1_value_1', 'tuple_1_value_2'), ('tuple_2_value_1', 'tuple_2_value_2')] })
			assert stringify.stringify(command) == 'some_command_type;some_key=[tuple_1_value_1,tuple_1_value_2|tuple_2_value_1,tuple_2_value_2]*'.encode()

		def test_ignores_connection_key(self):
			command = command_module.Command('some_command_type', { 'connection': 'some_connection'})
			assert stringify.stringify(command) == 'some_command_type*'.encode()

	class TestDestringify():
		def test_interprets_first_value_as_type(self):
			command = stringify.destringify('some_command_type*'.encode())
			assert command[0].type == 'some_command_type'

		def test_interprets_multiple_commands(self):
			command = stringify.destringify('some_command_type*some_other_command_type*'.encode())
			assert command[0].type == 'some_command_type'
			assert command[1].type == 'some_other_command_type'

		def test_interprets_data_strings(self):
			command = stringify.destringify('some_command_type;some_key=some_value*'.encode())
			assert command[0].data == { 'some_key': 'some_value' }

		def test_interprets_data_lists_of_strings(self):
			command = stringify.destringify('some_command_type;some_key=[some_value_1|some_value_2]*'.encode())
			assert command[0].data == { 'some_key': ['some_value_1', 'some_value_2'] }

		def test_interprets_data_lists_of_tuples(self):
			command = stringify.destringify('some_command_type;some_key=[tuple_1_value_1,tuple_1_value_2|tuple_2_value_1,tuple_2_value_2]*'.encode())
			assert command[0].data == { 'some_key': [('tuple_1_value_1', 'tuple_1_value_2'), ('tuple_2_value_1', 'tuple_2_value_2')] }
