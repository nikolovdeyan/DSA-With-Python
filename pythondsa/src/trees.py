from pythondsa.src.singly_linked import LinkedQueue


class Tree:
    """Abstract base class representing a tree structure."""

    class Position:
        """An abstraction representing the location of a single element."""

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            raise NotImplementedError('must be implemented by subclass')

    #   ------------------ Abstract methods ---------------------
    def root(self):
        """Return Position representing the tree's root (or None if empty)."""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        """Return Position representing p's parent (or None if p is root)."""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError('must be implemented by subclass')

    #   ------------------ Concrete methods ---------------------
    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for p in self.positions():
            yield p.element()

    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.preorder()

    def is_root(self, p):
        """Return True if Postition p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def depth(self, p):
        """Returns the number of levels separating position p from the root."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def preorder(self):
        """Generate a preorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def breadthfirst(self):
        """Generate a breadth-first iteration of the positions of the tree."""
        if not self.is_empty():
            fringe = LinkedQueue()
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                p = fringe.dequeue()
                yield p
                for c in self.children(p):
                    fringe.enqueue(c)

    def _height(self, p=None):
        """Returns the height of the subtree rooted at position p.

        If p is None return the hight of the entire tree.
        """
        if p is None:
            p = self.root()
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height(c) for c in self.children(p))

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def _subtree_postorder(self, p):
        """Generate a postorder iteration of positions in subtree rooted at p."""
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p


class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure."""
    #   ------------------ Abstract methods ---------------------
    def left(self, p):
        """Returns a Position representing p's left child.

        Returns None if p does not have a left child.
        """
        raise NotImplementedError('Must be implemented by subclass.')

    def right(self, p):
        """Returns a Position representing p's right child.

        Returns None if p does not have a right child.
        """
        raise NotImplementedError('Must be implemented by subclass.')

    #   ----------------- Overriden methods ---------------------
    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.inorder()  # overriden method to make inorder the default traversal.

    #   ------------------ Concrete methods ---------------------
    def sibling(self, p):
        """Returns a position representing p's sibling.

        Returns None if p has no sibling.
        """
        parent = self.parent(p)
        if parent is None:  # then p must be root
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """Generate an iteration of positions representing p's children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.left(p) is not None:  # if left child exists, traverse its subtree
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p                        # visit p between its subtrees
        if self.right(p) is not None:  # if right child exists, traverse its subtree
            for other in self._subtree_inorder(self.right(p)):
                yield other


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    class _Node:
        """A lightweight, nonpublic class for storing a node."""

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Returns the element stored at this position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def __len__(self):
        """Returns the total number of elements in the tree."""
        return self._size

    def root(self):
        """Returns the root Position of the tree.

        Returns None if the tree is empty.
        """
        return self._make_position(self._root)

    def parent(self, p):
        """Returns the Position of p's parent.

        Returns None if p is root.
        """
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """Returns the Position of p's left child.

        Returns None if p has no left child.
        """
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Returns the Position of p's right child.

        Returns None if p has no right child.
        """
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Returns the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:  # left child exists
            count += 1
        if node._right is not None:  # right child exists
            count += 1
        return count

    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:
            raise ValueError('p is no longer valud')
        return p._node

    def _make_position(self, node):
        """Returns a Position instance for a given node.

        Returns None if no node.
        """
        return self.Position(self, node) if node is not None else None

    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.

        Raise ValueError if the tree is not empty.
        """
        if self._root is not None:
            raise ValueError('Root exists.')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        """Create a new left child for Position p, storing element e.
        Returns the Position of the new node.

        Raises ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists.')
        self._size += 1
        node._left = self._Node(e, node)
        return self._make_position(node._left)

    def _add_right(self, p, e):
        """Create a new right child for Position p, storing element e.
        Returns the Position of the new node.

        Raises ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child exists.')
        self._size += 1
        node._right = self._Node(e, node)
        return self._make_position(node._right)

    def _replace(self, p, e):
        """Replace the element at Position p with e, and return the old element."""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        """Delete the node at Position p, and replace it with its child, if any.
        Returns the element that had been stored at Posititon p.

        Raises ValueError if Position p is invalid or p already has two children.
        """
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p already has two children.')
        child = node._left if node._left else node._right  # can be None
        if child is not None:
            child._parent = node._parent  # grandparent becomes parent
        if node is self._root:
            self._root = child  # the child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('Position must be leaf.')
        if not type(self) is type(t1) is type(t2):  # all trees must be the same type
            raise TypeError('The tree types must match.')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():  # attached t1 as left subtree
            t1._root._parent = node
            node._left = t1._root
            t1._root = None  # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():  # attached t2 as right subtree
            t2._root._parent = node
            node._right = t2._root
            t2._root = None  # set t2 instance to empty
            t2._size = 0
