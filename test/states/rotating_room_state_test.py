import pytest
import pyglet
from src.states import no_selection_state as no_selection_state_module, rotating_room_state as rotating_room_state_module, state_machine as state_machine_module
from src.utils import grid_position as grid_position_module

class TestRotatingRoomState():
	class TestIsRotating():
		def test_returns_true_if_grid_position_matches(self):
			rotating_room_state = rotating_room_state_module.RotatingRoomState([], grid_position_module.GridPosition(1, 2), grid_position_module.LEFT)
			assert rotating_room_state.is_rotating(grid_position_module.GridPosition(1, 2)) == True

		def test_returns_false_if_grid_position_does_not_match(self):
			rotating_room_state = rotating_room_state_module.RotatingRoomState([], grid_position_module.GridPosition(1, 2), grid_position_module.LEFT)
			assert rotating_room_state.is_rotating(grid_position_module.GridPosition(1, 3)) == False

	class TestPlaceRoom():
		def test_transitions_to_no_selection_state(self):
			state_machine = state_machine_module.StateMachine([], [], [])
			rotating_room_state = rotating_room_state_module.RotatingRoomState(state_machine, grid_position_module.GridPosition(1, 2), grid_position_module.LEFT)
			state_machine.current_state = rotating_room_state
			rotating_room_state.place_room()
			assert state_machine.current_state.__class__ == no_selection_state_module.NoSelectionState
		