import pytest
import pyglet
from src.common import attribute_set
import config

class TestAttributeSet():
	def test_sets_attribute_values_to_defaults(self):
		character = attribute_set.AttributeSet(
			speed=config.CHARACTERS[0]['speed'],
			speed_index=config.CHARACTERS[0]['speed_index'],
			might=config.CHARACTERS[0]['might'],
			might_index=config.CHARACTERS[0]['might_index'],
			sanity=config.CHARACTERS[0]['sanity'],
			sanity_index=config.CHARACTERS[0]['sanity_index'],
			knowledge=config.CHARACTERS[0]['knowledge'],
			knowledge_index=config.CHARACTERS[0]['knowledge_index']
		)
		expected_speed = config.CHARACTERS[0]['speed'][config.CHARACTERS[0]['speed_index']]
		expected_might = config.CHARACTERS[0]['might'][config.CHARACTERS[0]['might_index']]
		expected_sanity = config.CHARACTERS[0]['sanity'][config.CHARACTERS[0]['sanity_index']]
		expected_knowledge = config.CHARACTERS[0]['knowledge'][config.CHARACTERS[0]['knowledge_index']]
		assert character.get_attribute_value('speed') == expected_speed
		assert character.get_attribute_value('might') == expected_might
		assert character.get_attribute_value('sanity') == expected_sanity
		assert character.get_attribute_value('knowledge') == expected_knowledge

	def test_allows_changing_attribute_value(self):
		character = attribute_set.AttributeSet(
			speed=config.CHARACTERS[0]['speed'],
			speed_index=config.CHARACTERS[0]['speed_index'],
			might=config.CHARACTERS[0]['might'],
			might_index=config.CHARACTERS[0]['might_index'],
			sanity=config.CHARACTERS[0]['sanity'],
			sanity_index=config.CHARACTERS[0]['sanity_index'],
			knowledge=config.CHARACTERS[0]['knowledge'],
			knowledge_index=config.CHARACTERS[0]['knowledge_index']
		)
		character.change_attribute_value('speed', 3)
		expected_speed = config.CHARACTERS[0]['speed'][config.CHARACTERS[0]['speed_index'] + 3]
		assert character.get_attribute_value('speed') == expected_speed

	def test_allows_changing_attribute_value_negatively(self):
		character = attribute_set.AttributeSet(
			speed=config.CHARACTERS[0]['speed'],
			speed_index=config.CHARACTERS[0]['speed_index'],
			might=config.CHARACTERS[0]['might'],
			might_index=config.CHARACTERS[0]['might_index'],
			sanity=config.CHARACTERS[0]['sanity'],
			sanity_index=config.CHARACTERS[0]['sanity_index'],
			knowledge=config.CHARACTERS[0]['knowledge'],
			knowledge_index=config.CHARACTERS[0]['knowledge_index']
		)
		character.change_attribute_value('speed', -2)
		expected_speed = config.CHARACTERS[0]['speed'][config.CHARACTERS[0]['speed_index'] - 2]
		assert character.get_attribute_value('speed') == expected_speed

	def test_allows_max_index_of_8(self):
		character = attribute_set.AttributeSet(
			speed=config.CHARACTERS[0]['speed'],
			speed_index=config.CHARACTERS[0]['speed_index'],
			might=config.CHARACTERS[0]['might'],
			might_index=config.CHARACTERS[0]['might_index'],
			sanity=config.CHARACTERS[0]['sanity'],
			sanity_index=config.CHARACTERS[0]['sanity_index'],
			knowledge=config.CHARACTERS[0]['knowledge'],
			knowledge_index=config.CHARACTERS[0]['knowledge_index']
		)
		character.change_attribute_value('speed', 15)
		expected_speed = config.CHARACTERS[0]['speed'][8]
		assert character.get_attribute_value('speed') == expected_speed

	def test_allows_min_index_of_0(self):
		character = attribute_set.AttributeSet(
			speed=config.CHARACTERS[0]['speed'],
			speed_index=config.CHARACTERS[0]['speed_index'],
			might=config.CHARACTERS[0]['might'],
			might_index=config.CHARACTERS[0]['might_index'],
			sanity=config.CHARACTERS[0]['sanity'],
			sanity_index=config.CHARACTERS[0]['sanity_index'],
			knowledge=config.CHARACTERS[0]['knowledge'],
			knowledge_index=config.CHARACTERS[0]['knowledge_index']
		)
		character.change_attribute_value('speed', -15)
		expected_speed = config.CHARACTERS[0]['speed'][0]
		assert character.get_attribute_value('speed') == expected_speed

	def test_is_dead_if_any_attribute_is_at_0_index(self):
		character = attribute_set.AttributeSet(
			speed=config.CHARACTERS[0]['speed'],
			speed_index=config.CHARACTERS[0]['speed_index'],
			might=config.CHARACTERS[0]['might'],
			might_index=config.CHARACTERS[0]['might_index'],
			sanity=config.CHARACTERS[0]['sanity'],
			sanity_index=config.CHARACTERS[0]['sanity_index'],
			knowledge=config.CHARACTERS[0]['knowledge'],
			knowledge_index=config.CHARACTERS[0]['knowledge_index']
		)
		character.change_attribute_value('sanity', -15)
		assert character.is_dead()


