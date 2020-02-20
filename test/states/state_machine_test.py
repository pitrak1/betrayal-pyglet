import pytest
import pyglet
from src.states import state_machine as state_machine_module, no_selection_state as no_selection_state_module

class TestStateMachine():
	def test_starts_in_no_selection_state(self):
		state_machine = state_machine_module.StateMachine([], [], [])
		assert state_machine.current_state.__class__ == no_selection_state_module.NoSelectionState
		