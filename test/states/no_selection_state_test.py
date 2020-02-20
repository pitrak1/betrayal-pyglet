import pytest
import pyglet
from src.states import no_selection_state as no_selection_state_module, selected_state as selected_state_module, state_machine as state_machine_module

class TestNoSelectionState():
	class TestSelect():
		def test_transitions_to_selected_state(self):
			state_machine = state_machine_module.StateMachine([], [], [])
			no_selection_state = no_selection_state_module.NoSelectionState(state_machine)
			state_machine.current_state = no_selection_state
			no_selection_state.select('selected')
			assert state_machine.current_state.__class__ == selected_state_module.SelectedState
			assert state_machine.current_state.selected == 'selected'
		