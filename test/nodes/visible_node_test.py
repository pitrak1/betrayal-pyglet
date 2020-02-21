import pytest
import pyglet
from src.nodes import visible_node as visible_node_module
from src.states import commands as commands_module, selected_state as selected_state_module, state_machine as state_machine_module, no_selection_state as no_selection_state_module
from src.utils import grid_position as grid_position_module, position as position_module

@pytest.mark.usefixtures('make_character_tile', 'make_selected_state')
class TestVisibleNode():
	class TestOnDraw():
		def test_calls_on_draw_with_false_if_not_selected_state(self, mocker, make_character_tile):
			visible_node = visible_node_module.VisibleNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 1))
			mocker.patch.object(visible_node.tile, 'on_draw')
			state = no_selection_state_module.NoSelectionState(state_machine_module.StateMachine([], [], []))
			visible_node.on_draw(state)
			visible_node.tile.on_draw.assert_called_once_with(False)

		def test_calls_on_draw_with_false_if_selected_state_and_not_selected(self, mocker, make_character_tile, make_selected_state):
			visible_node = visible_node_module.VisibleNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 1))
			mocker.patch.object(visible_node.tile, 'on_draw')
			state = make_selected_state(mocker, selected=visible_node)
			mocker.patch.object(state, 'is_selected', return_value=False)
			visible_node.on_draw(state)
			visible_node.tile.on_draw.assert_called_once_with(False)

		def test_calls_on_draw_with_true_if_selected_state_and_selected(self, mocker, make_character_tile, make_selected_state):
			visible_node = visible_node_module.VisibleNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 1))
			mocker.patch.object(visible_node.tile, 'on_draw')
			state = make_selected_state(mocker, selected=visible_node)
			mocker.patch.object(state, 'is_selected', return_value=True)
			visible_node.on_draw(state)
			visible_node.tile.on_draw.assert_called_once_with(True)
