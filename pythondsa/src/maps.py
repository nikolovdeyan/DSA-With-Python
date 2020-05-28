from random import randrange
from collections.abc import MutableMapping
from pythondsa.src.trees import LinkedBinaryTree


class MapBase(MutableMapping):
    """Our own abstract base class that includes a nonpublic _Item class."""

    class _Item:
        """Lightweight composite to store key-value pairs as map items."""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key


class HashMapBase(MapBase):
    """Abstract base class for map using hash-table with MAD compression."""

    def __init__(self, cap=11, p=109345121):
        """Create an empty hash-table map."""
        self._table = cap * [None]
        self._n = 0
        self._prime = p
        self._scale = 1 + randrange(p - 1)
        self._shift = randrange(p)

    def _hash_function(self, k):
        return (hash(k) * self._scale + self._shift) % self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        j = self._hash_function(k)
        return self._bucket_getitem(j, k)

    def __setitem__(self, k, v):
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v)
        # Keep load factor <= 0.5
        if self._n > len(self._table) // 2:
            # number 2^x - 1 is often prime
            self._resize(2 * len(self._table) - 1)

    def __delitem__(self, k):
        j = self._hash_function(k)
        self._bucket_delitem(j, k)
        self._n -= 1

    def _resize(self, c):
        old = list(self.items())
        self._table = c * [None]
        self._n = 0
        for (k, v) in old:
            self[k] = v


class UnsortedTableMap(MapBase):
    """Map implementation using an unordered list."""

    def __init__(self):
        """Create an empty map."""
        self._table = []

    def __getitem__(self, k):
        """Return value associated with key k.

        Raise KeyError if k is not found.
        """
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, k, v):
        """Assign value to key k, overwriting existing value if present."""
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):
        """Remove item associated with key k.

        Raise KeyError if k is not found.
        """
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)
                return
        raise KeyError('Key Error: ' + repr(k))

    def __len__(self):
        """Return number of items in the map."""
        return len(self._table)

    def __iter__(self):
        """Generate iterations of the map's keys."""
        for item in self._table:
            yield item._key


class ChainHashMap(HashMapBase):
    """Hash map implemented with separate chaining for collision resolution."""

    def _bucket_getitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k))
        return bucket[k]

    def _bucket_setitem(self, j, k, v):
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize:
            self._n += 1

    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k))
        del bucket[k]

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:
                    yield key


class ProbeHashMap(HashMapBase):
    """Hash map implemented with linear probing for collision resolution."""
    _AVAIL = object()  # sentinel marks locations of previous deletions

    def _is_available(self, j):
        """Return True if index j is available in table."""
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _find_slot(self, j, k):
        """Search for key k in bucket at index j.

        Return (success, index) tuple, described as follows:
        - if match was found, success is True and index denotes its location.
        - if no match found, success is False and index denotes first available slot.
        """
        first_avail = None
        while True:
            if self._is_available(j):
                if first_avail is None:     # mark this as first available
                    first_avail = j
                if self._table[j] is None:  # search has failed
                    return (False, first_avail)
            elif k == self._table[j]._key:  # found a match
                return (True, j)
            j = (j + 1) % len(self._table)  # keep looking

    def _bucket_getitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError('Key Error: ' + repr(k))
        return self._table[s]._value

    def _bucket_setitem(self, j, k, v):
        found, s = self._find_slot(j, k)
        if not found:
            self._table[s] = self._Item(k, v)
            self._n += 1
        else:
            self._table[s]._value = v

    def _bucket_delitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError('Key Error: ' + repr(k))
        self._table[s] = ProbeHashMap._AVAIL  # mark as vacated

    def __iter__(self):
        for j in range(len(self._table)):
            if not self._is_available(j):
                yield self._table[j]._key


class SortedTableMap(MapBase):
    """Map implementation using a sorted table."""

    # ------------------------- nonpublic behaviours -------------------------------
    def _find_index(self, k, low, high):
        """Return index of the leftmost item with key greater than or equal to k.

        Return high + 1 if no such item qualifies.

        That is, j will be returned such that:
           - all items of slice table [low:j] have key < k
           - all items of slice table [j:high+1] have key >= k
        """
        if high < low:
            return high + 1  # no element qualifies
        else:
            mid = (low + high) // 2
            if k == self._table[mid]._key:
                return mid  # found exact match
            elif k < self._table[mid]._key:
                return self._find_index(k, low, mid - 1)  # may return mid
            else:
                return self._find_index(k, mid + 1, high)  # answer is right of mid

    # --------------------------- public behaviours --------------------------------
    def __init__(self):
        """Create an empty map."""
        self._table = []

    def __len__(self):
        """Return number of items in the map."""
        return len(self._table)

    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))
        return self._table[j]._value

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            self._table[j]._value = v                # reassign value
        else:
            self._table.insert(j, self._Item(k, v))  # add new item

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ', + repr(k))
        self._table.pop(j)

    def __iter__(self):
        """Generate keys of the map ordered from minimum to maximum."""
        for item in self._table:
            yield item._key

    def __reversed__(self):
        """Generate keys of the map ordered from maximum to minimum."""
        for item in reversed(self._table):
            yield item._key

    def find_min(self):
        """Return (key, value) pair with minimum key (or None if empty)."""
        if len(self._table) > 0:
            return (self._table[0]._key, self._table[0]._value)
        else:
            return None

    def find_max(self):
        """Return (key, value) pair with maximum key (or None if empty)."""
        if len(self._table) > 0:
            return (self._table[-1]._key, self._table[-1]._value)
        else:
            return None

    def find_ge(self, k):
        """Return (key, value) pair with least key greater than or equal to k."""
        j = self._find_index(k, 0, len(self._table) - 1)  # j's key >= k
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_lt(self, k):
        """Return (key, value) pair with greatest key strictly less than k."""
        j = self._find_index(k, 0, len(self._table) - 1)  # j's key >= k
        if j > 0:
            return (self._table[j - 1]._key, self._table[j - 1]._value)
        else:
            return None

    def find_gt(self, k):
        """Return (key, value) pair with least key strictly greater than k."""
        j = self._find_index(k, 0, len(self._table) - 1)  # j's key >= k
        if j < len(self._table) and self._table[j]._key == k:
            j += 1  # advanced past match
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that start <= key < stop.

        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if start is None:
            j = 0
        else:
            j = self._find_index(start, 0, len(self._table) - 1)  # find first result
        while j < len(self._table) and (stop is None or self._table[j]._key < stop):
            yield (self._table[j]._key, self._table[j]._value)
            j += 1


class MultiMap:
    """A multimap class built upon use of an underlying map for storage."""
    _MapType = dict  # Map type; can be redefined by subclass

    def __init__(self):
        """Create a new empty multimap instance."""
        self._map = self._MapType()  # a map instance for storage
        self._n = 0

    def __len__(self):
        """Return the number of items stored in the multimap."""
        return self._n

    def __iter__(self):
        """Iterate through all (k, v) pairs in multimap."""
        for k, secondary in self._map.items():
            for v in secondary:
                yield (k, v)

    def add(self, k, v):
        """Add pair (k, v) to the multimap."""
        container = self._map.setdefault(k, [])  # create an empty list, if needed
        container.append(v)
        self._n += 1

    def pop(self, k):
        """Remove and return arbitrary (k, v) with key k (or raise KeyError)."""
        secondary = self._map[k]  # may raise KeyError
        v = secondary.pop()
        if len(secondary) == 0:
            del self._map[k]  # if no pairs left, delete key
        self._n -= 1
        return (k, v)

    def find(self, k):
        """Return arbitrary (k, v) pair with given key (or raise KeyError)."""
        secondary = self._map[k]  # may raise KeyError
        return (k, secondary[0])

    def find_all(self, k):
        """Generate iteration of all (k, v) pairs with given key."""
        secondary = self._map.get(k, [])  # empty list by default
        for v in secondary:
            yield (k, v)


class TreeMap(LinkedBinaryTree, MapBase):
    """Sorted map implementation using a binary search tree."""

    # --------------------- override Position class ---------------------
    class Position(LinkedBinaryTree.Position):
        def key(self):
            """Return key of map's key-value pair."""
            return self.element()._key

        def value(self):
            """Return value of map's key-value pair."""
            return self.element()._value

    # ------------------------ nonpublic utilities -----------------------
    def _subtree_search(self, p, k):
        """Return Position of p's subtree having key k, or last node searched."""
        if k == p.key():   # found a match
            return p
        elif k < p.key():  # search left subtree
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
            else:          # search right subtree
                if self.right(p) is not None:
                    return self._subtree_search(self.right(p), k)
            return p       # unsuccessful search

    def _subtree_first_position(self, p):
        """Return Position of first item in subtree rooted at p."""
        walk = p
        while self.left(walk) is not None:  # keep walking left
            walk = self.left(walk)
        return walk

    def _subtree_last_position(self, p):
        """Return Position of last item in subtree rooted at p."""
        walk = p
        while self.right(walk) is not None:  # keep walking right
            walk = self.right(walk)
        return walk

    def first(self):
        """Return the first Position in the tree (or None if empty)."""
        return self._subtree_first_position(self.root()) if len(self) > 0 else None

    def last(self):
        """Return the last Position in the tree (or None if empty)."""
        return self._subtree_last_position(self.root()) if len(self) > 0 else None

    def before(self, p):
        """Return the Position just before p in the natural order.

        Return None if p is the first position.
        """
        self._validate(p)  # inherited from LinkedBinaryTree
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:  # walk upward
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):
        """Return the Position just after p in the natural order.

        Return None if p is the last position.
        """
        self._validate(p)
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        """Return position with key k, or else neighbor (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)  # hook for balanced tree subclasses
            return p

    def find_min(self):
        """Return (key, value) pair with minimum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_ge(self, k):
        """Return (key, value) pair with least key greater than or equal to k.

        Return None if there does not exist such a key.
        """
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)  # may not find exact match
            if p.key() < k:  # p's key is too small
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that start <= key < stop.

        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                #  we initialize p with logic similar to find_ge
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)

    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        if self.is_empty():
            raise KeyError('Key Error: ' + repr(k))
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)  # hook for balanced tree subclasses
            if k != p.key():
                raise KeyError('Key Error: ' + repr(k))
            return p.value()

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))  # from LinkedBinaryTree
        else:
            p = self._subtree_search(self.root(), k)
            if p.key() == k:
                p.element()._value = v  # replace existing item's value
                self._rebalance_access(p)  # hook for balanced tree subclasses
                return
            else:
                item = self._Item(k, v)
                if p.key() < k:
                    leaf = self._add_right(p, item)  # inherited from LinkedBinaryTree
                else:
                    leaf = self._add_left(p, item)  # inherited from LinkedBinaryTree
        self._rebalance_insert(leaf)  # hook for balanced tree subclasses

    def __iter__(self):
        """Generate an iteration of all keys in the map in order."""
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)

    def delete(self, p):
        """Remove the item at given Position."""
        self._validate(p)  # inherited from LinkedBinaryTree
        if self.left(p) and self.right(p):  # if p has two children
            replacement = self._subtree_last_position(self.left(p))
            self._replace(p, replacement.element())
            p = replacement
        #  now p has at most one child
        parent = self.parent(p)
        self._delete(p)  # inherited from LinkedBinaryTree
        self._rebalance_delete(parent)  # if root deleted, parent is None

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                self.delete(p)  # rely on positional version
                return
            self._rebalance_access(p)  # hook for balanced tree subclasses
        raise KeyError('Key Error: ' + repr(k))
