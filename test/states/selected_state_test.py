import pytest
import pyglet
from src.states import commands as commands_module, selected_state as selected_state_module, rotating_room_state as rotating_room_state_module, state_machine as state_machine_module
from src.utils import grid_position as grid_position_module

@pytest.mark.usefixtures("make_room_tile_stack")
class TestSelectedState():
	class TestSelected():
		def test_sets_selected(self):
			selected_state = selected_state_module.SelectedState([], None)
			selected_state.select('selected')
			assert selected_state.selected == 'selected'

	class TestIsSelected():
		def test_returns_true_if_argument_matches(self):
			selected_state = selected_state_module.SelectedState([], 'selected')
			assert selected_state.is_selected('selected') == True

		def test_returns_false_if_argument_does_not_match(self):
			selected_state = selected_state_module.SelectedState([], 'selected')
			assert selected_state.is_selected('other selected') == False

	class TestMove():
		def test_adds_command_to_move_selected_to_position(self):
			state_machine = state_machine_module.StateMachine([], [], [])
			selected_state = selected_state_module.SelectedState(state_machine, 'selected')
			selected_state.move(grid_position_module.GridPosition(1, 2))
			assert state_machine.command_queue[0].__class__ == commands_module.MoveCharacterCommand
			assert state_machine.command_queue[0].character == 'selected'
			assert state_machine.command_queue[0].grid_position == grid_position_module.GridPosition(1, 2)

	class TestMoveIntoNewRoom():
		def test_adds_command_to_add_room(self, mocker, make_room_tile_stack):
			state_machine = state_machine_module.StateMachine([], make_room_tile_stack(mocker), [])
			selected_state = selected_state_module.SelectedState(state_machine, 'selected')
			selected_state.move_into_new_room(grid_position_module.GridPosition(1, 2), grid_position_module.RIGHT)
			assert state_machine.command_queue[0].__class__ == commands_module.AddRoomCommand
			assert state_machine.command_queue[0].grid_position == grid_position_module.GridPosition(1, 2)
			assert state_machine.command_queue[0].rotation == 0

		def test_adds_command_to_move_selected(self, mocker, make_room_tile_stack):
			state_machine = state_machine_module.StateMachine([], make_room_tile_stack(mocker), [])
			selected_state = selected_state_module.SelectedState(state_machine, 'selected')
			selected_state.move_into_new_room(grid_position_module.GridPosition(1, 2), grid_position_module.RIGHT)
			assert state_machine.command_queue[1].__class__ == commands_module.MoveCharacterCommand
			assert state_machine.command_queue[1].character == 'selected'
			assert state_machine.command_queue[1].grid_position == grid_position_module.GridPosition(1, 2)

		def test_transitions_to_rotating_room_state(self, mocker, make_room_tile_stack):
			state_machine = state_machine_module.StateMachine([], make_room_tile_stack(mocker), [])
			selected_state = selected_state_module.SelectedState(state_machine, 'selected')
			selected_state.move_into_new_room(grid_position_module.GridPosition(1, 2), grid_position_module.RIGHT)
			assert state_machine.current_state.__class__ == rotating_room_state_module.RotatingRoomState
			assert state_machine.current_state.grid_position == grid_position_module.GridPosition(1, 2)
			assert state_machine.current_state.entering_direction == grid_position_module.RIGHT
		