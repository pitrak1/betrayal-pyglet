import pytest
from src.states import selected_state as selected_state_module, state_machine as state_machine_module

@pytest.fixture
def make_selected_state(make_character_node):
	def _make_selected_state(mocker, selected=None, grid_position=None):
		if not selected: selected = make_character_node(mocker, grid_position)
		state = selected_state_module.SelectedState(state_machine_module.StateMachine([], [], []), selected)
		mocker.patch.object(state, 'select')
		mocker.patch.object(state, 'is_selected')
		mocker.patch.object(state, 'move')
		mocker.patch.object(state, 'move_into_new_room')
		return state
	return _make_selected_state