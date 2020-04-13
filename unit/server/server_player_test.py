import pytest
import pyglet
from src.server import server_player
from src.common import command
import types

class TestServerPlayer():
	class TestEquality():
		def test_returns_true_if_connections_match_if_given_other_player(self, mocker):
			player_1 = server_player.ServerPlayer('player 1', True, 'some connection')
			player_2 = server_player.ServerPlayer('player 2', True, 'some connection')
			assert player_1 == player_2

		def test_returns_true_if_given_matching_connection(self, mocker):
			player_ = server_player.ServerPlayer('player name', True, 'some connection')
			assert player_ == 'some connection'

		def test_returns_false_if_connection_not_set(self, mocker):
			player_ = server_player.ServerPlayer('player name', True)
			assert player_ != None

