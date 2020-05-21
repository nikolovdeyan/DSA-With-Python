import ctypes
from pythondsa.src.exceptions import Empty


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty array."""
        self._n = 0                                 # count actual elements
        self._capacity = 1                          # default array capacity
        self._A = self._make_array(self._capacity)  # low-level array

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):
        """Return element at index k."""
        if not self._n * -1 <= k < self._n:
            raise IndexError('Invalid index')
        if k >= 0:
            return self._A[k]
        else:
            negative_index = self._n - self._capacity + k
            return self._A[negative_index]

    def append(self, obj):
        """Add object to the end of the array."""
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        self._A[self._n] = obj
        self._n += 1

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        #  (for simplicity, we assume 0 <= k <= n in this version)
        if self._n == self._capacity:  # array needs to be resized
            self._resize_with_shift(2 * self._capacity, k)
        else:  # no need to resize array
            for j in range(self._n, k, -1):
                self._A[j] = self._A[j - 1]
        self._A[k] = value
        self._n += 1

    def remove(self, value):
        """Remove first occurrence of value (or raise ValueError)."""
        for k in range(self._n):
            if self._A[k] == value:
                for j in range(k, self._n - 1):
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None        # help garbage collection
                self._n -= 1
                if self._capacity // 4 > self._n:   # shrink capacity if needed
                    self._resize(self._capacity // 2)
                return
        raise ValueError('value not found')    # only reached if no match

    def pop(self):
        """Remove and return the last element in the array.

        Raise Empty exception if the array is empty."""
        if self._n == 0:
            raise Empty('The array is empty')
        answer = self._A[self._n - 1]
        self._A[self._n - 1] = None  # help garbage collection
        self._n -= 1
        if self._capacity // 4 > self._n:  # shrink capacity if needed
            self._resize(self._capacity // 2)
        return answer

    def _resize(self, c):
        """Resize internal array to capacity c."""
        B = self._make_array(c)
        for k in range(self._n):
            B[k] = self._A[k]
        self._A = B
        self._capacity = c

    def _resize_with_shift(self, c, k):
        """Resize internal array to capacity c and shift elements after k rightward."""
        B = self._make_array(c)
        for i in range(k):
            B[i] = self._A[i]
        for i in range(k, self._n, 1):
            B[i + 1] = self._A[i]
        self._A = B
        self._capacity = c

    def _make_array(self, c):
        """Return new array with capacity c."""
        return (c * ctypes.py_object)()
