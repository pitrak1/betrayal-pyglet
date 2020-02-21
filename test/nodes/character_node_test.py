import pytest
import pyglet
from src.nodes import character_node as character_node_module
from src.states import commands as commands_module, selected_state as selected_state_module, state_machine as state_machine_module, no_selection_state as no_selection_state_module
from src.utils import grid_position as grid_position_module, position as position_module

@pytest.mark.usefixtures('make_character_tile', 'make_selected_state')
class TestCharacterNode():
	class TestTranslatedMousePressHandler():
		class TestWithSelectedState():
			def test_selects_if_in_bounds_and_lmb(self, mocker, make_character_tile, make_selected_state):
				character_node = character_node_module.CharacterNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 0))
				state = make_selected_state(mocker, grid_position=grid_position_module.GridPosition(1, 1))
				command = commands_module.TranslatedMousePressCommand(position_module.Position(0, 0), pyglet.window.mouse.LEFT, 'modifiers')
				assert character_node.on_command(command, state) == True
				state.select.assert_called_once_with(character_node)

			def test_does_not_select_if_not_in_bounds(self, mocker, make_character_tile, make_selected_state):
				character_node = character_node_module.CharacterNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 0))
				state = make_selected_state(mocker, grid_position=grid_position_module.GridPosition(1, 1))
				command = commands_module.TranslatedMousePressCommand(position_module.Position(1024, 1024), pyglet.window.mouse.LEFT, 'modifiers')
				assert character_node.on_command(command, state) == False
				state.select.assert_not_called()

			def test_does_not_select_if_not_lmb(self, mocker, make_character_tile, make_selected_state):
				character_node = character_node_module.CharacterNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 0))
				state = make_selected_state(mocker, grid_position=grid_position_module.GridPosition(1, 1))
				command = commands_module.TranslatedMousePressCommand(position_module.Position(0, 0), pyglet.window.mouse.RIGHT, 'modifiers')
				assert character_node.on_command(command, state) == False
				state.select.assert_not_called()

		class TestWithNoSelectionState():
			def test_selects_if_in_bounds_and_lmb(self, mocker, make_character_tile, make_selected_state):
				character_node = character_node_module.CharacterNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 0))
				state = no_selection_state_module.NoSelectionState(state_machine_module.StateMachine([], [], []))
				mocker.patch.object(state, 'select')
				command = commands_module.TranslatedMousePressCommand(position_module.Position(0, 0), pyglet.window.mouse.LEFT, 'modifiers')
				assert character_node.on_command(command, state) == True
				state.select.assert_called_once_with(character_node)

			def test_does_not_select_if_not_in_bounds(self, mocker, make_character_tile, make_selected_state):
				character_node = character_node_module.CharacterNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 0))
				state = no_selection_state_module.NoSelectionState(state_machine_module.StateMachine([], [], []))
				mocker.patch.object(state, 'select')
				command = commands_module.TranslatedMousePressCommand(position_module.Position(1024, 1024), pyglet.window.mouse.LEFT, 'modifiers')
				assert character_node.on_command(command, state) == False
				state.select.assert_not_called()

			def test_does_not_select_if_not_lmb(self, mocker, make_character_tile, make_selected_state):
				character_node = character_node_module.CharacterNode(make_character_tile(mocker), grid_position_module.GridPosition(0, 0))
				state = no_selection_state_module.NoSelectionState(state_machine_module.StateMachine([], [], []))
				mocker.patch.object(state, 'select')
				command = commands_module.TranslatedMousePressCommand(position_module.Position(0, 0), pyglet.window.mouse.RIGHT, 'modifiers')
				assert character_node.on_command(command, state) == False
				state.select.assert_not_called()

