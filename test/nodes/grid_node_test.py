import pytest
import pyglet
from src.nodes import grid_node as grid_node_module
from src.states import commands as commands_module, selected_state as selected_state_module, state_machine as state_machine_module
from src.utils import grid_position as grid_position_module, position as position_module

@pytest.mark.usefixtures('make_world_node', 'make_selected_state')
class TestGridNode():
	class TestMousePressHandler():
		class TestWithSelectedState():
			def test_does_not_move_if_not_right_mouse_button(self, mocker, make_world_node, make_selected_state):
				grid_node = grid_node_module.GridNode(grid_position_module.GridPosition(0, 0), make_world_node(mocker))
				state = make_selected_state(mocker, grid_position=grid_position_module.GridPosition(0, 1))
				command = commands_module.MousePressCommand(position_module.Position(0, 0), pyglet.window.mouse.LEFT, 'modifiers')
				grid_node.on_command(command, state)
				state.move_into_new_room.assert_not_called()

			def test_does_not_move_if_within_bounds(self, mocker, make_world_node, make_selected_state):
				grid_node = grid_node_module.GridNode(grid_position_module.GridPosition(0, 0), make_world_node(mocker))
				state = make_selected_state(mocker, grid_position=grid_position_module.GridPosition(0, 1))
				command = commands_module.MousePressCommand(position_module.Position(1024, 1024), pyglet.window.mouse.RIGHT, 'modifiers')
				grid_node.on_command(command, state)
				state.move_into_new_room.assert_not_called()

			def test_does_not_move_if_cannot_move(self, mocker, make_world_node, make_selected_state):
				grid_node = grid_node_module.GridNode(grid_position_module.GridPosition(0, 0), make_world_node(mocker))
				mocker.patch.object(grid_node.world, 'can_move', return_value=False)
				state = make_selected_state(mocker, grid_position=grid_position_module.GridPosition(0, 1))
				command = commands_module.MousePressCommand(position_module.Position(0, 0), pyglet.window.mouse.RIGHT, 'modifiers')
				grid_node.on_command(command, state)
				state.move_into_new_room.assert_not_called()

			def test_moves_into_new_room_if_rmb_within_bounds_and_can_move(self, mocker, make_world_node, make_selected_state):
				grid_node = grid_node_module.GridNode(grid_position_module.GridPosition(0, 0), make_world_node(mocker))
				state = make_selected_state(mocker, grid_position=grid_position_module.GridPosition(0, 1))
				command = commands_module.MousePressCommand(position_module.Position(0, 0), pyglet.window.mouse.RIGHT, 'modifiers')
				grid_node.on_command(command, state)
				state.move_into_new_room.assert_called_once_with(grid_position_module.GridPosition(0, 0), grid_position_module.DOWN)

	class TestWithinBounds():
		def test_calls_within_square_bounds_on_grid_position(self, mocker, make_world_node):
			grid_node = grid_node_module.GridNode(grid_position_module.GridPosition(0, 0), make_world_node(mocker))
			mocker.patch.object(grid_node.grid_position, 'within_square_bounds')
			grid_node.within_bounds(position_module.Position(15, 20))
			grid_node.grid_position.within_square_bounds.assert_called_once_with(position_module.Position(15, 20), grid_position_module.GRID_SIZE)
