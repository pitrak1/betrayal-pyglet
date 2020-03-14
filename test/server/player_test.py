import pytest
import pyglet
from src.server import player as player_module

class TestPlayer():
	class TestEq():
		def test_returns_true_if_given_player_with_same_connection(self):
			player = player_module.Player('name', 'host', 'connection')
			assert player == player_module.Player('other_name', 'other_host', 'connection')

		def test_returns_false_if_given_player_with_different_connection(self):
			player = player_module.Player('name', 'host', 'connection')
			assert player != player_module.Player('other_name', 'other_host', 'other_connection')

		def test_returns_true_if_given_matching_connection(self):
			player = player_module.Player('name', 'host', 'connection')
			assert player == 'connection'

		def test_returns_false_if_given_nonmatching_connection(self):
			player = player_module.Player('name', 'host', 'connection')
			assert player != 'other_connection'

		def test_returns_false_if_connection_is_none(self):
			player = player_module.Player('name', 'host', None)
			assert player != player_module.Player('name', 'host', None)
