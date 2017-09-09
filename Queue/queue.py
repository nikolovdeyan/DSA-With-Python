from empty import Empty


class Queue:
    """Queue implementation using a Python list as underlying storage."""

    DEFAULT_CAPACITY = 10  # moderate capacity for new queues

    def __init__(self):
        """Creates an empty queue."""
        self._data = [None] * Queue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        """Returns the number of elements in the queue."""
        return self._size

    def _resize(self, cap):
        """Resizes the list to capacity >= len(self)."""
        old = self._data                  # keep track of existing list
        self._data = [None] * cap
        walk = self._front

        for k in range(self._size):
            self._data[k] = old[walk]     # shift indices
            walk = (1 + walk) % len(old)  # old size used for modulus
        self._front = 0

    def is_empty(self):
        """Returns True if the queue is empty"""
        return self._size == 0

    def first(self):
        """
        Returns the lement at the front of the queue, without removing it.
        Raises Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('The queue is empty')
        return self._data[self._front]

    def enqueue(self, e):
        """Add an element to the back of the queue."""
        if self._size == len(self._data):
            self._resize(2 * len(self._data))  # double the array size

        last_in_line = (self._front + self._size) % len(self._data)
        self._data[last_in_line] = e
        self._size += 1

    def dequeue(self):
        """
        Removes and returns the element in front of the queue.
        Raises Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('The queue is empty')

        result = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1

        return result

