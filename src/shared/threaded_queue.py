import threading

class ThreadedQueue():
	def __init__(self):
		self.__queue = []
		self.__lock = threading.Lock()

	def has_elements(self):
		return len(self.__queue) > 0

	def pop_front(self):
		self.__lock.acquire()
		command = self.__queue.pop(0)
		self.__lock.release()
		return command

	def append(self, command):
		self.__lock.acquire()
		self.__queue.append(command)
		self.__lock.release()
