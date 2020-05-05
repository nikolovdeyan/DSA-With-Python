import unittest
from tree import LinkedBinaryTree, BinaryTree, Tree


class TestLinkedBinaryTreeMethods(unittest.TestCase):

    def test_len_returns_the_number_of_elements_in_tree(self):
        lt = LinkedBinaryTree()
        expected_result = 0

        result = len(lt)

        self.assertEqual(result, expected_result)

        lt._size = 1
        expected_result = 1

        result = len(lt)

        self.assertEqual(result, expected_result)

    def test_root_returns_none_with_empty_tree(self):
        lt = LinkedBinaryTree()

        result = lt.root()

        self.assertIsNone(result)

    def test_root_returns_the_root_position_of_the_tree(self):
        lt = LinkedBinaryTree()
        expected_element = 'foo'
        n = lt._Node(expected_element, None, None, None)
        lt._root = n
        lt._size = 1

        result = lt.root()

        self.assertIsNotNone(result)
        self.assertIs(result._node._element, expected_element)

    def test_parent_returns_none_if_position_is_root(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo')
        lt._size = 1
        root_position = lt.Position(lt, lt._root)

        result = lt.parent(root_position)

        self.assertIsNone(result)

    def test_parent_returns_position_parent_when_position_not_root(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo')
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._size = 2
        child_position = lt.Position(lt, lt._root._left)
        expected_result = lt.Position(lt, lt._root)

        result = lt.parent(child_position)

        self.assertEqual(result, expected_result)

    def test_left_returns_none_if_position_has_no_left_child(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo')
        lt._size = 1
        root_position = lt.Position(lt, lt._root)

        result = lt.left(root_position)

        self.assertIsNone(result)

    def test_left_returns_position_of_left_child(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo')
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._size = 2
        root_position = lt.Position(lt, lt._root)
        expected_result = lt.Position(lt, lt._root._left)

        result = lt.left(root_position)

        self.assertEqual(result, expected_result)

    def test_right_returns_none_if_position_has_no_right_child(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo')
        lt._size = 1
        root_position = lt.Position(lt, lt._root)

        result = lt.right(root_position)

        self.assertIsNone(result)

    def test_right_returns_position_of_right_child(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo')
        lt._root._right = lt._Node('bar', lt._root, None, None)
        lt._size = 2
        root_position = lt.Position(lt, lt._root)
        expected_result = lt.Position(lt, lt._root._right)

        result = lt.right(root_position)

        self.assertEqual(result, expected_result)

    def test_num_children_returns_number_of_children_nodes_of_position(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo')
        lt._size = 1
        expected_result = 0
        root_position = lt.Position(lt, lt._root)

        result = lt.num_children(root_position)

        self.assertEqual(result, expected_result)

        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._root._right = lt._Node('baz', lt._root, None, None)
        lt._size = 3
        expected_result = 2

        result = lt.num_children(root_position)

        self.assertEqual(result, expected_result)

    def test_validate_raises_TypeError_with_parameter_not_Position(self):
        lt = LinkedBinaryTree()
        wrong_type = 'foo'

        self.assertRaises(TypeError, lt._validate, wrong_type)

    def test_validate_raises_ValueError_with_Position_from_different_container(self):
        lt = LinkedBinaryTree()
        other_lt = LinkedBinaryTree()
        bad_position = other_lt.Position(other_lt, other_lt._Node('foo'))

        self.assertRaises(ValueError, lt._validate, bad_position)

    def test_validate_raises_ValueError_with_deprecated_node(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo')
        lt._root._left = lt._Node('bar', None, None, None)
        lt._root._left._parent = lt._root._left  # deprecate node
        lt._size = 2
        bad_position = lt.Position(lt, lt._root._left)

        self.assertRaises(ValueError, lt._validate, bad_position)

    def test_add_root_raises_ValueError_with_nonempty_tree(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._size = 1

        self.assertRaises(ValueError, lt._add_root, 'foo')

    def test_add_root_places_element_at_root_of_empty_tree_returns_Position(self):
        lt = LinkedBinaryTree()
        element = 'foo'

        result = lt._add_root(element)

        self.assertIsInstance(result, lt.Position)
        self.assertIs(lt._root._element, element)
        self.assertIs(result._node._element, element)

    def test_add_left_raises_ValueError_with_nonempty_node(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._size = 2
        root_position = lt.Position(lt, lt._root)

        self.assertRaises(ValueError, lt._add_left, root_position, 'foo')

    def test_add_left_stores_element_as_left_child_returns_Position(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._size = 1
        root_position = lt.Position(lt, lt._root)
        expected_element = 'bar'

        result_position = lt._add_left(root_position, expected_element)

        self.assertIsInstance(result_position, lt.Position)
        self.assertIs(result_position._node._element, expected_element)
        self.assertIs(root_position._node._left._element, expected_element)

    def test_add_right_raises_ValueError_with_nonempty_node(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._right = lt._Node('bar', lt._root, None, None)
        lt._size = 2
        root_position = lt.Position(lt, lt._root)

        self.assertRaises(ValueError, lt._add_right, root_position, 'foo')

    def test_add_right_stores_element_as_right_child_returns_Position(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._size = 1
        root_position = lt.Position(lt, lt._root)
        expected_element = 'bar'

        result_position = lt._add_right(root_position, expected_element)

        self.assertIsInstance(result_position, lt.Position)
        self.assertIs(result_position._node._element, expected_element)
        self.assertIs(root_position._node._right._element, expected_element)

    def test_replace_replaces_element_at_Position_returns_old_element(self):
        lt = LinkedBinaryTree()
        old_element = 'bar'
        new_element = 'baz'
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node(old_element, lt._root, None, None)
        lt._size = 2
        pos_to_replace = lt.Position(lt, lt._root._left)

        result_element = lt._replace(pos_to_replace, new_element)

        self.assertIs(pos_to_replace._node._element, new_element)
        self.assertIs(result_element, old_element)

    def test_delete_raises_ValueError_when_called_on_Position_with_two_children(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._root._left._left = lt._Node('baz', lt._root._left, None, None)
        lt._root._left._right = lt._Node('spam', lt._root._left, None, None)
        lt._size = 4
        pos_to_delete = lt.Position(lt, lt._root._left)

        self.assertRaises(ValueError, lt._delete, pos_to_delete)

    def test_delete_deletes_node_on_Position_replaces_with_a_single_child(self):
        lt = LinkedBinaryTree()
        element_to_delete = 'bar'
        child_element = 'baz'
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node(element_to_delete, lt._root, None, None)
        lt._root._left._left = lt._Node(child_element, lt._root._left, None, None)
        lt._size = 3
        pos_to_delete = lt.Position(lt, lt._root._left)

        deleted_element = lt._delete(pos_to_delete)

        self.assertIs(deleted_element, element_to_delete)
        self.assertIs(lt._root._left._element, child_element)
        self.assertIs(lt._root._left._parent, lt._root)

    def test_attach_raises_ValueError_when_Position_not_a_leaf(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', None, None, None)
        lt._root._right = lt._Node('baz', None, None, None)
        lt._size = 3

        lt_left = LinkedBinaryTree()
        lt_right = LinkedBinaryTree()

        invalid_position = lt.Position(lt, lt._root)

        self.assertRaises(ValueError, lt._attach, invalid_position, lt_left, lt_right)

    def test_attach_raises_TypeError_when_different_tree_types_provided(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', None, None, None)
        lt._size = 2

        lt_left = BinaryTree()
        lt_right = Tree()

        attach_position = lt.Position(lt, lt._root._left)

        self.assertRaises(TypeError, lt._attach, attach_position, lt_left, lt_right)

    def test_attach_attaches_subtrees_as_left_and_right_children_of_Position(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', None, None, None)
        lt._size = 2
        branch_left = LinkedBinaryTree()
        branch_left._root = branch_left._Node('spam', None, None)
        branch_left._size = 1
        branch_right = LinkedBinaryTree()
        branch_right._root = branch_right._Node('eggs', None, None)
        branch_right._size = 1
        attach_position = lt.Position(lt, lt._root._left)

        lt._attach(attach_position, branch_left, branch_right)

        self.assertEqual(lt._size, 4)
        self.assertIs(attach_position._node._left._element, 'spam')
        self.assertIs(attach_position._node._right._element, 'eggs')
        self.assertIs(attach_position._node._left._parent, attach_position._node)
        self.assertIs(attach_position._node._right._parent, attach_position._node)
        self.assertEqual(branch_left._size, 0)
        self.assertEqual(branch_right._size, 0)

    #  Test Tree ABC's concrete methods:
    def test_TreeABC_is_root_returns_correct_boolean_values(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._size = 2
        root_position = lt.Position(lt, lt._root)
        non_root_position = lt.Position(lt, lt._root._left)

        self.assertTrue(lt.is_root(root_position))
        self.assertFalse(lt.is_root(non_root_position))

    def test_TreeABC_is_leaf_returns_correct_boolean_values(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._size = 2
        root_position = lt.Position(lt, lt._root)
        non_root_position = lt.Position(lt, lt._root._left)

        self.assertTrue(lt.is_leaf(non_root_position))
        self.assertFalse(lt.is_leaf(root_position))

    def test_TreeABC_is_empty_returns_correct_boolean_values(self):
        lt_empty = LinkedBinaryTree()
        lt_non_empty = LinkedBinaryTree()
        lt_non_empty._root = lt_non_empty._Node('foo', None, None, None)
        lt_non_empty._size = 1

        self.assertTrue(lt_empty.is_empty())
        self.assertFalse(lt_non_empty.is_empty())

    def test_TreeABC_depth_returns_number_of_levels_from_Position_to_root(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._root._left._left = lt._Node('baz', lt._root._left, None, None)
        lt._size = 3
        expected_result = 2
        position = lt.Position(lt, lt._root._left._left)

        result = lt.depth(position)

        self.assertEqual(result, expected_result)

    def test_TreeABC_height_returns_height_of_subtree_at_Position(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._root._left._left = lt._Node('baz', lt._root._left, None, None)
        lt._root._left._left._right = lt._Node('spam', lt._root._left._left, None, None)
        lt._size = 4
        expected_result = 3
        position = lt.Position(lt, lt._root)

        result = lt._height(position)

        self.assertEqual(result, expected_result)

    #  Test BinaryTree ABC's concrete methods:
    def test_BinaryTreeABC_sibling_returns_None_on_position_with_no_sibling(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', None, None, None)
        lt._size = 2
        only_child_position = lt.Position(lt, lt._root._left)

        result_position = lt.sibling(only_child_position)

        self.assertIsNone(result_position)

    def test_BinaryTreeABC_sibling_returns_other_sibling_Position(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._root._right = lt._Node('baz', lt._root, None, None)
        lt._size = 3
        left_child_position = lt.Position(lt, lt._root._left)
        right_child_position = lt.Position(lt, lt._root._right)

        lefts_sibling_position = lt.sibling(left_child_position)
        rights_sibling_position = lt.sibling(right_child_position)

        self.assertEqual(lefts_sibling_position, right_child_position)
        self.assertEqual(rights_sibling_position, left_child_position)

    def test_BinaryTreeABC_children_returns_iteration_of_Position_children(self):
        lt = LinkedBinaryTree()
        lt._root = lt._Node('foo', None, None, None)
        lt._root._left = lt._Node('bar', lt._root, None, None)
        lt._root._right = lt._Node('baz', lt._root, None, None)
        lt._size = 3
        parent_position = lt.Position(lt, lt._root)

        children_generator = lt.children(parent_position)
        first_result = next(children_generator)
        second_result = next(children_generator)

        self.assertEqual(first_result, lt.Position(lt, lt._root._left))
        self.assertEqual(second_result, lt.Position(lt, lt._root._right))
        self.assertRaises(StopIteration, children_generator.__next__)
