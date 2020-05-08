from pythondsa.src.exceptions import Empty, Full


class ArrayStack:
    """Stack implementation using a Python list as underlying storage."""

    def __init__(self, maxlen=None):
        """Creates an empty stack."""
        self._data = []
        self._maxlen = maxlen

    def __len__(self):
        """Returns the number of elements in the stack."""
        return len(self._data)

    def is_empty(self):
        """Returns True if the stack is empty."""
        return len(self._data) == 0

    def is_full(self):
        """Returns True if the stack is full."""
        return len(self._data) == self._maxlen

    def push(self, e):
        """Adds an element to the top of the stack.

        Raises Full exception if the stack has assigned maxlen and is full.
        """
        if self.is_full():
            raise Full('Tre stack is full')
        self._data.append(e)

    def top(self):
        """
        Returns the element at the top of the stack, without removing it.
        Raises Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('The stack is empty')
        return self._data[-1]

    def pop(self):
        """
        Removes and returns the element from the top of the stack.
        Raises Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('The stack is empty')
        return self._data.pop()

