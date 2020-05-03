import unittest
from tree import LinkedBinaryTree


class TestLinkedBinaryTreeMethods(unittest.TestCase):

    # The tree can be empty (without any nodes).
    def test_constructor_creates_an_empty_tree(self):
        t = LinkedBinaryTree()

        self.assertIsInstance(t, LinkedBinaryTree)

    def test_empty_tree_size_should_be_zero(self):
        t = LinkedBinaryTree()
        expected_size = 0
        actual_size = t._size

        self.assertEqual(actual_size, expected_size)

    # is_empty() should return True if the tree is empty
    # validate()

    def test_is_empty_should_return_true_if_tree_is_empty(self):
        t = LinkedBinaryTree()

        self.assertTrue(t.is_empty())

    # If a tree is nonempty it has a special node called the root. The root has no parent.
    def test_add_root_stores_element_returns_position(self):
        t = LinkedBinaryTree()
        element = 'r'

        t._add_root(element)
        # directly access the root
        pos = t._make_position(t._root)

        # add_root returns Position
        self.assertIsInstance(pos, LinkedBinaryTree.Position)
        # The returned position stores the element
        self.assertEqual(element, pos._node._element)

    def test_root_returns_none_with_empty_tree(self):
        t = LinkedBinaryTree()

        result = t.root()

        self.assertIsNone(result)



# Each node of the tree that is no root has an unique parent node and is a child of that node.

