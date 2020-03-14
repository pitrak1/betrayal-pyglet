import pytest
import pyglet
from src.shared import threaded_queue

class TestThreadedQueue():
	class TestHasElements():
		def test_returns_true_if_queue_length_greater_than_zero(self):
			queue = threaded_queue.ThreadedQueue()
			queue.append(True)
			assert queue.has_elements()

		def test_returns_false_if_queue_length_is_zero(self):
			queue = threaded_queue.ThreadedQueue()
			assert not queue.has_elements()

	class TestPopFront():
		def test_returns_first_element_in_queue(self):
			queue = threaded_queue.ThreadedQueue()
			queue.append(True)
			assert queue.pop_front() == True

		def test_raises_error_if_queue_is_empty(self):
			queue = threaded_queue.ThreadedQueue()
			with pytest.raises(IndexError) as exception:
				queue.pop_front()
			assert str(exception.value) == 'pop from empty list'
