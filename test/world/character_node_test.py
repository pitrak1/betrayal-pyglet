import pytest
import pyglet
from pyglet import sprite
from src.world import character_node

class TestCharacterNode():
	class TestConstructor():
		def test_creates_sprite(self, mocker, make_character_node):
			make_character_node(mocker)
			sprite.Sprite.assert_called_once_with('image', 0, 0)

	class TestOnDraw():
		def test_draws_sprite(self, mocker, make_character_node):
			node = make_character_node(mocker)
			node.on_draw()
			node.sprite.draw.assert_called_once()
    