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


class LinkedStack:
    """LIFO Stack implementation using a singly linked list for storage."""

    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = '_element', '_next'  # streamline memory usage

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        """Create an empty stack."""
        self._head = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in the stack."""
        return self._size

    def is_empty(self):
        """Return True if the stack is empty."""
        return self._size == 0

    def push(self, e):
        """Add element e to the top of the stack."""
        self._head = self._Node(e, self._head)
        self._size += 1

    def top(self):
        """Return (but do not remove) the element at the top of the stack.

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element  # top of stack is at head of list

    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        return answer
