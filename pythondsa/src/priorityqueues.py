from pythondsa.src.exceptions import Empty
from pythondsa.src.lists import PositionalList


class PriorityQueueBase:
    """Abstract base class for a priority queue."""

    class _Item:
        """Lightweight composite to store priority queue items."""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key

        def __eq__(self, other):
            return self._key == other._key and self._value == other._value

    def is_empty(self):
        """Return True if the priority queue is empty."""
        return len(self) == 0


class UnsortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with an unsorted list."""

    def _find_min(self):
        """Return Position of item with minimum key."""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            if walk.element() < small.element():
                small = walk
            walk = self._data.after(walk)
        return small

    def __init__(self):
        """Create a new empty Priority Queue."""
        self._data = PositionalList()

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, key, value):
        """Add a key-value pair."""
        self._data.add_last(self._Item(key, value))

    def min(self):
        """Return but do not remove (k, v) tuple with minimum key."""
        p = self._find_min()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (k, v) tuple with minimum key from the prioriry queue."""
        p = self._find_min()
        item = self._data.delete(p)
        return (item._key, item._value)


class SortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a sorted list."""

    def __init__(self):
        """Create a new empty Priority Queue."""
        self._data = PositionalList()

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, key, value):
        """Add a key-value pair."""
        newest = self._Item(key, value)
        walk = self._data.last()  # walk backward looking for smaller key
        while walk is not None and newest < walk.element():
            walk = self._data.before(walk)
        if walk is None:
            self._data.add_first(newest)        # new key is the smallest
        else:
            self._data.add_after(walk, newest)  # newest goes after walk

    def min(self):
        """Return but do not remove (k, v) tuple with minimum key."""
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        p = self._data.first()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (k, v) tuple with minimum key from the priority queue."""
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        item = self._data.delete(self._data.first())
        return (item._key, item._value)


class HeapPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a binary heap."""
    # ------------------- nonpublic behaviours ------------------------
    def _parent(self, j):
        return (j - 1) // 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        """Swap the elements at indices i and j of array."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[small_child] < self._data[j]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    def _heapify(self):
        start = self._parent(len(self) - 1)  # start at PARENT of last leaf
        for j in range(start, -1, -1):       # going to and including the root
            self._downheap(j)

    #  --------------------- public behaviours -------------------------
    def __init__(self, contents=()):
        """Create a new empty Priority Queue.

        By default, queue will be empty. If contents is given, it should be as an
        iterable sequence of (k, v) tuples specifying the initial contents.
        """
        self._data = [self._Item(k, v) for k, v in contents]
        if len(self._data) > 1:
            self._heapify()

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._data)

    def add(self, key, value):
        """Add a key-value pair to the priority queue."""
        self._data._append(self._Item(key, value))
        self._upheap(len(self._data) - 1)  # upheap the newly added position

    def min(self):
        """Return but do not remove (k, v) tuple with minimum key.

        Raise Empty exception if empty.
        """
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        """Remove and return (k, v) tuple with minimum key.

        Raise Empty exception if empty.
        """
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        self._swap(0, len(self._data) - 1)  # put minimum item at the end
        item = self._data.pop()             # remove the minimum item from the list
        self._downheap(0)                   # fix the new root
        return (item._key, item._value)
