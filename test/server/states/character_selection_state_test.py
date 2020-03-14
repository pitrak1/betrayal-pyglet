import pytest
import pyglet
from src.server.states import lobby_state as lobby_state_module, character_selection_state as character_selection_state_module
from src.shared import command as command_module
import config

@pytest.mark.usefixtures('make_character_selection_state')
class TestLobbyState():
	class TestNetworkGetPlayerOrderHandler():
		def test_sends_success_response(self, mocker, make_character_selection_state):
			state = make_character_selection_state(mocker, 3)
			command = command_module.Command('network_get_player_order', { 'connection': 'player connection 0' })
			state.network_get_player_order_handler(command)
			command_module.update_and_send.assert_called_once_with(command, { 'status': 'success', 'players': ['player 0', 'player 2', 'player 1'] })

	class TestNetworkConfirmPlayerOrderHandler():
		class TestWhenCalledForEachPlayer():
			def test_sends_response_to_all_players(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_confirm_player_order')
				state.network_confirm_player_order_handler(command)
				state.network_confirm_player_order_handler(command)
				state.network_confirm_player_order_handler(command)
				command_module.update_and_send.assert_has_calls([
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 0' }),
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 2' }),
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 1' })
				], any_order=True)

		class TestWhenCalledOnce():
			def test_does_not_send_response(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_confirm_player_order')
				state.network_confirm_player_order_handler(command)
				command_module.update_and_send.assert_not_called()

	class TestNetworkGetAvailableCharactersHandler():
		def test_sends_response(self, mocker, make_character_selection_state):
			state = make_character_selection_state(mocker, 3)
			command = command_module.Command('network_get_available_characters')
			state.network_get_available_characters_handler(command)
			command_module.update_and_send.assert_called_once_with(command, { 'status': 'success', 'characters': [character['variable_name'] for character in config.STARTING_CHARACTERS] })

	class TestNetworkGetCurrentPlayerHandler():
		class TestWhenCalledByCurrentPlayer():
			def test_sends_response_with_self(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_get_current_player', { 'connection': 'player connection 1'})
				state.network_get_current_player_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'success', 'player_name': 'self' })

		class TestWhenNotCalledByCurrentPlayer():
			def test_sends_response_with_self(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_get_current_player', { 'connection': 'player connection 0'})
				state.network_get_current_player_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'success', 'player_name': 'player 1' })

	class TestNetworkSelectCharacterHandler():
		class TestWhenCalledByCurrentPlayer():
			def test_sets_player_character(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_select_character', { 'connection': 'player connection 1', 'character': 'heather_granville'})
				state.network_select_character_handler(command)
				assert next(p for p in state.players if p.name == 'player 1').character.variable_name == 'heather_granville'

			def test_removes_available_character(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_select_character', { 'connection': 'player connection 1', 'character': 'heather_granville'})
				state.network_select_character_handler(command)
				assert sum(c for c in state.characters if c.variable_name == 'heather_granville') == 0

			def test_sends_success_response(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_select_character', { 'connection': 'player connection 1', 'character': 'heather_granville'})
				state.network_select_character_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'success' })

			class TestIfLastPlayerToSelect():
				def test_sends_completion_response_to_all_players(self, mocker, make_character_selection_state):
					state = make_character_selection_state(mocker, 3)
					command = command_module.Command('network_select_character', { 'connection': 'player connection 0', 'character': 'heather_granville'})
					state.current_player_index = 0
					state.network_select_character_handler(command)
					command_module.create_and_send.assert_has_calls([
						mocker.call('network_all_characters_selected', { 'status': 'success', 'connection': 'player connection 0' }),
						mocker.call('network_all_characters_selected', { 'status': 'success', 'connection': 'player connection 2' }),
						mocker.call('network_all_characters_selected', { 'status': 'success', 'connection': 'player connection 1' })
					], any_order=True)

			class TestIfNotLastPlayerToSelect():
				def test_sends_update_response_to_all_players(self, mocker, make_character_selection_state):
					state = make_character_selection_state(mocker, 3)
					command = command_module.Command('network_select_character', { 'connection': 'player connection 1', 'character': 'heather_granville'})
					state.network_select_character_handler(command)
					command_module.create_and_send.assert_has_calls([
						mocker.call('network_get_current_player', { 'status': 'success', 'player_name': 'player 2', 'connection': 'player connection 0' }),
						mocker.call('network_get_current_player', { 'status': 'success', 'player_name': 'player 2', 'connection': 'player connection 2' }),
						mocker.call('network_get_current_player', { 'status': 'success', 'player_name': 'player 2', 'connection': 'player connection 1' }),
						mocker.call('network_get_available_characters', { 'status': 'success', 'characters': [c.variable_name for c in state.characters], 'connection': 'player connection 0' }),
						mocker.call('network_get_available_characters', { 'status': 'success', 'characters': [c.variable_name for c in state.characters], 'connection': 'player connection 2' }),
						mocker.call('network_get_available_characters', { 'status': 'success', 'characters': [c.variable_name for c in state.characters], 'connection': 'player connection 1' })
					], any_order=True)

		class TestWhenNotCalledByCurrentPlayer():
			def test_sends_not_current_player_response(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_select_character', { 'connection': 'player connection 0'})
				state.network_select_character_handler(command)
				command_module.update_and_send.assert_called_once_with(command, { 'status': 'not_current_player' })

	class TestNetworkGetCharacterSelectionsHandler():
		def test_sends_response(self, mocker, make_character_selection_state):
			state = make_character_selection_state(mocker, 3)
			command = command_module.Command('network_get_character_selections')
			state.players[0].character = state.characters[0]
			state.players[1].character = state.characters[3]
			state.network_get_character_selections_handler(command)
			command_module.update_and_send.assert_called_once_with(command, { 'status': 'success', 'selections': [(p.name, p.character.display_name if p.character else None) for p in state.players] })

	class TestNetworkConfirmCharacterSelectionsHandler():
		class TestWhenCalledForEachPlayer():
			def test_sends_response_to_all_players(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_confirm_character_selections')
				state.network_confirm_character_selections_handler(command)
				state.network_confirm_character_selections_handler(command)
				state.network_confirm_character_selections_handler(command)
				command_module.update_and_send.assert_has_calls([
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 0' }),
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 2' }),
					mocker.call(command, { 'status': 'success', 'connection': 'player connection 1' })
				], any_order=True)

		class TestWhenCalledOnce():
			def test_does_not_send_response(self, mocker, make_character_selection_state):
				state = make_character_selection_state(mocker, 3)
				command = command_module.Command('network_confirm_character_selections')
				state.network_confirm_character_selections_handler(command)
				command_module.update_and_send.assert_not_called()
