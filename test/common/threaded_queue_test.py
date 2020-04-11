import pytest
import pyglet
from src.common import threaded_queue

class TestThreadedQueue():
	def test_has_no_elements_on_initialization(self):
		queue = threaded_queue.ThreadedQueue()
		assert not queue.has_elements()

	def test_allows_adding_elements(self):
		queue = threaded_queue.ThreadedQueue()
		queue.append(True)
		assert queue.has_elements()

	def test_allows_popping_elements(self):
		queue = threaded_queue.ThreadedQueue()
		queue.append('some command')
		assert queue.pop_front() == 'some command'

	def test_raises_error_if_queue_is_empty(self):
		queue = threaded_queue.ThreadedQueue()
		with pytest.raises(IndexError) as exception:
			queue.pop_front()
