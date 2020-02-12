import pytest
import pyglet
from pyglet import sprite, window
from src.world import character_node
from src.commands import commands
from src.state import state_machine

class TestCharacterNode():
	class TestConstructor():
		def test_creates_sprite_and_selected_sprite(self, mocker, make_character_node):
			make_character_node(mocker)
			sprite.Sprite.assert_called_with('image', 0, 0)
			assert sprite.Sprite.call_count == 2

	class TestOnDraw():
		def test_draws_sprite_if_not_selected(self, mocker, make_character_node):
			node = make_character_node(mocker)
			node.on_draw()
			node.sprite.draw.assert_called_once()

		def test_draws_selected_sprite_if_selected(self, mocker, make_character_node):
			node = make_character_node(mocker)
			node.state_machine.current_state = state_machine.SelectedState(node)
			node.on_draw()
			node.sprite_selected.draw.assert_called_once()

	class TestOnCommand():
		class TestWithMousePressCommand():
			class TestWhenButtonIsLeftMouseButton():
				class TestWhenWithinBounds():
					def test_calls_select_on_state_machine(self, mocker, make_stubbed_state_machine, make_character_node):
						node = make_character_node(mocker, 30, 40)
						x = 30 + (character_node.CHARACTER_SIZE - 10) // 2
						command = commands.MousePressCommand(x=x, y=40, button=window.mouse.LEFT, modifiers=[])
						node.on_command(command)
						node.state_machine.select.assert_called_once_with(node)

					def test_returns_true(self, mocker, make_stubbed_state_machine, make_character_node):
						node = make_character_node(mocker, 30, 40)
						x = 30 + (character_node.CHARACTER_SIZE - 10) // 2
						command = commands.MousePressCommand(x=x, y=40, button=window.mouse.LEFT, modifiers=[])
						assert node.on_command(command) == True

				class TestWhenNotWithinBounds():
					def test_does_not_call_select_on_state_machine(self, mocker, make_stubbed_state_machine, make_character_node):
						node = make_character_node(mocker, 30, 40)
						x = 30 + (character_node.CHARACTER_SIZE + 10) // 2
						command = commands.MousePressCommand(x=x, y=40, button=window.mouse.LEFT, modifiers=[])
						node.on_command(command)
						node.state_machine.select.assert_not_called()

					def test_returns_false(self, mocker, make_stubbed_state_machine, make_character_node):
						node = make_character_node(mocker, 30, 40)
						x = 30 + (character_node.CHARACTER_SIZE + 10) // 2
						command = commands.MousePressCommand(x=x, y=40, button=window.mouse.LEFT, modifiers=[])
						assert node.on_command(command) == False
					
    