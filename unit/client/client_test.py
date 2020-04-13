import pytest
import pyglet
from src.client import client
from src.common import command
import types

class TestClient():
	class TestNetworkCreatePlayerHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_player', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_create_player_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_next_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_player', { 'status': 'success', 'player_name': 'some player name' })
			state = create_generic_state(mocker)
			client_.network_create_player_handler(command_, state)
			state.next.assert_called_once_with('some player name')

		def test_calls_state_invalid_player_name_when_status_is_invalid_player_name(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_player', { 'status': 'invalid_player_name' })
			state = create_generic_state(mocker)
			client_.network_create_player_handler(command_, state)
			state.invalid_player_name.assert_called_once()

		def test_calls_state_name_too_short_when_status_is_name_too_short(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_player', { 'status': 'name_too_short' })
			state = create_generic_state(mocker)
			client_.network_create_player_handler(command_, state)
			state.name_too_short.assert_called_once()

		def test_calls_state_name_too_long_when_status_is_name_too_long(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_player', { 'status': 'name_too_long' })
			state = create_generic_state(mocker)
			client_.network_create_player_handler(command_, state)
			state.name_too_long.assert_called_once()

	class TestNetworkCreateGameHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_game', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_create_game_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_next_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_game', { 'status': 'success', 'game_name': 'some game name' })
			state = create_generic_state(mocker)
			client_.network_create_game_handler(command_, state)
			state.next.assert_called_once_with('some game name')

		def test_calls_state_invalid_game_name_when_status_is_invalid_game_name(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_game', { 'status': 'invalid_game_name' })
			state = create_generic_state(mocker)
			client_.network_create_game_handler(command_, state)
			state.invalid_game_name.assert_called_once()

		def test_calls_state_name_too_short_when_status_is_name_too_short(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_game', { 'status': 'name_too_short' })
			state = create_generic_state(mocker)
			client_.network_create_game_handler(command_, state)
			state.name_too_short.assert_called_once()

		def test_calls_state_name_too_long_when_status_is_name_too_long(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_create_game', { 'status': 'name_too_long' })
			state = create_generic_state(mocker)
			client_.network_create_game_handler(command_, state)
			state.name_too_long.assert_called_once()

	class TestNetworkLeaveGameHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_leave_game', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_leave_game_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_back_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_leave_game', { 'status': 'success' })
			state = create_generic_state(mocker)
			client_.network_leave_game_handler(command_, state)
			state.back.assert_called_once()

	class TestNetworkGetPlayersInGameHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_players_in_game', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_get_players_in_game_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_set_players_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_players_in_game', { 'status': 'success', 'players': [] })
			state = create_generic_state(mocker)
			client_.network_get_players_in_game_handler(command_, state)
			state.set_players.assert_called_once_with([])

	class TestNetworkGetGamesHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_games', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_get_games_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_set_games_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_games', { 'status': 'success', 'games': [] })
			state = create_generic_state(mocker)
			client_.network_get_games_handler(command_, state)
			state.set_games.assert_called_once_with([])

	class TestNetworkJoinGameHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_join_game', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_join_game_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_next_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_join_game', { 'status': 'success', 'game_name': 'some game name' })
			state = create_generic_state(mocker)
			client_.network_join_game_handler(command_, state)
			state.next.assert_called_once_with('some game name')

		def test_calls_state_game_full_when_status_is_game_full(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_join_game', { 'status': 'game_full' })
			state = create_generic_state(mocker)
			client_.network_join_game_handler(command_, state)
			state.game_full.assert_called_once()

	class TestNetworkLogoutHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_logout', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_logout_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_exit_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_logout', { 'status': 'success' })
			state = create_generic_state(mocker)
			client_.network_logout_handler(command_, state)
			state.exit.assert_called_once()

	class TestNetworkStartGameHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_start_game', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_start_game_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_next_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_start_game', { 'status': 'success' })
			state = create_generic_state(mocker)
			client_.network_start_game_handler(command_, state)
			state.next.assert_called_once()

		def test_calls_state_not_enough_players_when_status_is_not_enough_players(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_start_game', { 'status': 'not_enough_players' })
			state = create_generic_state(mocker)
			client_.network_start_game_handler(command_, state)
			state.not_enough_players.assert_called_once()

	class TestNetworkGetPlayerOrderHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_player_order', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_get_player_order_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_set_player_order_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_player_order', { 'status': 'success', 'players': [] })
			state = create_generic_state(mocker)
			client_.network_get_player_order_handler(command_, state)
			state.set_player_order.assert_called_once_with([])

	class TestNetworkConfirmPlayerOrderHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_confirm_player_order', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_confirm_player_order_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_next_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_confirm_player_order', { 'status': 'success' })
			state = create_generic_state(mocker)
			client_.network_confirm_player_order_handler(command_, state)
			state.next.assert_called_once()

	class TestNetworkGetAvailableCharactersHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_available_characters', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_get_available_characters_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_set_available_characters_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_available_characters', { 'status': 'success', 'characters': [] })
			state = create_generic_state(mocker)
			client_.network_get_available_characters_handler(command_, state)
			state.set_available_characters.assert_called_once_with([])

	class TestNetworkGetCurrentPlayerHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_current_player', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_get_current_player_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_set_current_player_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_current_player', { 'status': 'success', 'player_name': 'some player name' })
			state = create_generic_state(mocker)
			client_.network_get_current_player_handler(command_, state)
			state.set_current_player.assert_called_once_with('some player name')

	class TestNetworkSelectCharacterHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_select_character', { 'status': 'pending' })
			client_.network_select_character_handler(command_, None)
			command.send.assert_called_once_with(command_, None)

	class TestNetworkAllCharactersSelectedHandler():
		def test_calls_state_next_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_all_characters_selected', { 'status': 'success' })
			state = create_generic_state(mocker)
			client_.network_all_characters_selected_handler(command_, state)
			state.next.assert_called_once()

	class TestNetworkGetCharacterSelectionsHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_character_selections', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_get_character_selections_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_set_character_selections_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_character_selections', { 'status': 'success', 'selections': [] })
			state = create_generic_state(mocker)
			client_.network_get_character_selections_handler(command_, state)
			state.set_character_selections.assert_called_once_with([])

	class TestNetworkConfirmCharacterSelectionsHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_confirm_character_selections', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_confirm_character_selections_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_next_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_confirm_character_selections', { 'status': 'success' })
			state = create_generic_state(mocker)
			client_.network_confirm_character_selections_handler(command_, state)
			state.next.assert_called_once()

	class TestNetworkGetPlayerPositionsHandler():
		def test_sends_command_when_status_is_pending(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_player_positions', { 'status': 'pending' })
			state = create_generic_state(mocker)
			client_.network_get_player_positions_handler(command_, state)
			command.send.assert_called_once_with(command_, None)

		def test_calls_state_set_player_positions_when_status_is_success(self, mocker, create_generic_state):
			client_ = client.Client(mocker.stub(), testing=True)
			command_ = command.Command('network_get_player_positions', { 'status': 'success', 'players': [] })
			state = create_generic_state(mocker)
			client_.network_get_player_positions_handler(command_, state)
			state.set_player_positions.assert_called_once_with([])
