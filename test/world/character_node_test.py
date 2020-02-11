import pytest
import pyglet
from pyglet import sprite, window
from src.world import character_node
from src.commands import mouse_press_command, highlight_command

class TestCharacterNode():
	class TestConstructor():
		def test_creates_sprite_and_highlighted_sprite(self, mocker, make_character_node):
			make_character_node(mocker)
			sprite.Sprite.assert_called_with('image', 0, 0)
			assert sprite.Sprite.call_count == 2

	class TestOnDraw():
		def test_draws_sprite(self, mocker, make_character_node):
			node = make_character_node(mocker)
			node.on_draw()
			node.sprite.draw.assert_called_once()

		def test_draws_highlighted_sprite_if_highlighted(self, mocker, make_character_node):
			node = make_character_node(mocker)
			node.highlighted = True
			node.on_draw()
			node.sprite_highlighted.draw.assert_called_once()

	class TestOnCommand():
		class TestWithMousePressCommand():
			class TestWhenButtonIsLeftMouseButton():
				class TestWhenWithinBounds():
					def test_appends_highlight_command_to_queue(self, mocker, make_list, make_character_node):
						node = make_character_node(mocker, 30, 40)
						x = 30 + (character_node.CHARACTER_SIZE - 10) // 2
						command = mouse_press_command.MousePressCommand(x=x, y=40, button=window.mouse.LEFT, modifiers=[])
						queue = make_list(mocker)
						node.on_command(command, queue)
						queue.append.assert_called_once()
						assert queue.append.call_args[0][0].node == node

					def test_returns_true(self, mocker, make_list, make_character_node):
						node = make_character_node(mocker, 30, 40)
						x = 30 + (character_node.CHARACTER_SIZE - 10) // 2
						command = mouse_press_command.MousePressCommand(x=x, y=40, button=window.mouse.LEFT, modifiers=[])
						assert node.on_command(command, make_list(mocker)) == True

				class TestWhenNotWithinBounds():
					def test_does_not_append_to_queue(self, mocker, make_list, make_character_node):
						node = make_character_node(mocker, 30, 40)
						x = 30 + (character_node.CHARACTER_SIZE + 10) // 2
						command = mouse_press_command.MousePressCommand(x=x, y=40, button=window.mouse.LEFT, modifiers=[])
						queue = make_list(mocker)
						node.on_command(command, queue)
						queue.append.assert_not_called()

					def test_returns_false(self, mocker, make_list, make_character_node):
						node = make_character_node(mocker, 30, 40)
						x = 30 + (character_node.CHARACTER_SIZE + 10) // 2
						command = mouse_press_command.MousePressCommand(x=x, y=40, button=window.mouse.LEFT, modifiers=[])
						assert node.on_command(command, make_list(mocker)) == False

		class TestWithHighlightCommand():
			def test_sets_highlighted_if_given_self(self, mocker, make_character_node):
				node = make_character_node(mocker)
				command = highlight_command.HighlightCommand(node)
				node.on_command(command, [command])
				assert node.highlighted == True

			def test_resets_highlighted_if_not_given_self(self, mocker, make_character_node):
				node = make_character_node(mocker)
				other_node = make_character_node(mocker)
				command = highlight_command.HighlightCommand(other_node)
				node.on_command(command, [command])
				assert node.highlighted == False
					
    