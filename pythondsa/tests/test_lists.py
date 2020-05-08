import unittest
from unittest.mock import MagicMock
from pythondsa.src.lists import _DoublyLinkedBase, PositionalList


class Test_DoublyLinkedBaseMethods(unittest.TestCase):

    def test_constructor_initializes_the_list(self):
        expected_type = _DoublyLinkedBase._Node
        expected_size = 0

        ll = _DoublyLinkedBase()

        self.assertIsInstance(ll._header, expected_type)
        self.assertIsInstance(ll._trailer, expected_type)
        self.assertEqual(ll._size, expected_size)
        self.assertIs(ll._header._next, ll._trailer)
        self.assertIs(ll._trailer._prev, ll._header)

    def test_len_returns_the_number_of_elements_in_the_list(self):
        ll = _DoublyLinkedBase()
        self.assertEqual(len(ll), 0)

        # directly manipulating ._size property which __len__ uses:
        ll._size = 10
        self.assertEqual(len(ll), 10)

    def test_is_empty_returns_proper_boolean(self):
        ll = _DoublyLinkedBase()
        self.assertTrue(ll.is_empty())

        # manipulating directly ._size which is used by is_empty():
        ll._size = 1
        self.assertFalse(ll.is_empty())

    def test_insert_between_returns_correct_node(self):
        ll = _DoublyLinkedBase()
        #  create an empty Node to insert
        element = 'foo'

        new_position = ll._insert_between(element, ll._header, ll._trailer)

        #  affirm the returned node has correct references:
        self.assertIs(new_position._next, ll._trailer)
        self.assertIs(new_position._prev, ll._header)
        #  affirm the node is between the sentinels:
        self.assertIs(ll._header._next, new_position)
        self.assertIs(ll._trailer._prev, new_position)

    def test_delete_node_updates_correct_references(self):
        ll = _DoublyLinkedBase()
        #  setup a node detween the sentinels of the list:
        expected_element = 'foo'
        n = _DoublyLinkedBase._Node(expected_element, ll._header, ll._trailer)
        ll._header._next = n
        ll._trailer._prev = n
        ll._size = 1

        deleted_element = ll._delete_node(n)

        #  check the return value:
        self.assertIs(deleted_element, expected_element)
        #  check size of the list is updated:
        self.assertEqual(ll._size, 0)
        #  check sentinels reference each other:
        self.assertIs(ll._header._next, ll._trailer)
        self.assertIs(ll._trailer._prev, ll._header)


class TestPositionalListMethods(unittest.TestCase):

    def test_Position_constructor_creates_position_properties(self):
        #  create a container to host the position:
        container = PositionalList()
        #  create a node to be stored in the position:
        node = PositionalList._Node(None, None, None)

        p = PositionalList.Position(container, node)

        self.assertIs(p._container, container)
        self.assertIs(p._node, node)

    def test_Position_element_returns_the_element_stored_at_position(self):
        #  create a container to host the position:
        container = PositionalList()
        #  create a node to be stored in the position:
        expected_element = 'foo'
        node = PositionalList._Node(expected_element, None, None)
        p = PositionalList.Position(container, node)

        returned_element = p.element()

        self.assertIs(expected_element, returned_element)

    def test_Position_equals_returns_proper_boolean(self):
        #  create a container for the positions:
        container = PositionalList()
        #  create two nodes with proper references in the container:
        n1 = PositionalList._Node('foo', container._header, None)
        n2 = PositionalList._Node('bar', n1, container._trailer)
        n1._next = n2
        container._header._next = n1
        container._trailer._prev = n2
        #  create a position for each respective node:
        p1 = PositionalList.Position(container, n1)
        p2 = PositionalList.Position(container, n2)

        self.assertFalse(p1 == p2)

    def test_Position_not_equals_returns_proper_boolean(self):
        #  create a container for the positions:
        container = PositionalList()
        #  create two nodes with proper references in the container:
        n1 = PositionalList._Node('foo', container._header, None)
        n2 = PositionalList._Node('bar', n1, container._trailer)
        n1._next = n2
        container._header._next = n1
        container._trailer._prev = n2
        #  create a position for each respective node:
        p1 = PositionalList.Position(container, n1)
        p2 = PositionalList.Position(container, n2)

        self.assertTrue(p1 != p2)

    def test_validate_raises_TypeError_with_wrong_type(self):
        pl = PositionalList()
        wrong_type = PositionalList._Node(None, None, None)

        self.assertRaises(TypeError, pl._validate, wrong_type)

    def test_validate_raises_ValueError_with_wrong_container(self):
        #  create two containers
        pl1 = PositionalList()
        pl2 = PositionalList()
        n = PositionalList._Node(None, pl1._header, pl1._trailer)
        #  create a Position that is external to the container
        bad_position = PositionalList.Position(pl1, n)

        self.assertRaises(ValueError, pl2._validate, bad_position)

    def test_validate_raises_ValueError_with_invalidated_position(self):
        pl = PositionalList()
        #  the node has None as _next reference
        n = PositionalList._Node(None, pl._header, None)

        bad_position = PositionalList.Position(pl, n)

        self.assertRaises(ValueError, pl._validate, bad_position)

    def test_validate_returns_correct_node_with_correct_parameters(self):
        pl = PositionalList()
        #  setup a correctly referenced _Node:
        expected_node = PositionalList._Node('foo', pl._header, pl._trailer)
        pl._header._next = expected_node
        pl._trailer._prev = expected_node
        good_position = PositionalList.Position(pl, expected_node)

        result_node = pl._validate(good_position)

        self.assertIs(result_node, expected_node)

    def test_make_position_returns_None_with_sentinel_node_parameter(self):
        pl = PositionalList()
        header_node = pl._header
        trailer_node = pl._trailer

        result_header = pl._make_position(header_node)
        result_trailer = pl._make_position(trailer_node)

        self.assertIsNone(result_header)
        self.assertIsNone(result_trailer)

    def test_make_position_returns_Position_instance_for_given_node(self):
        pl = PositionalList()
        n = PositionalList._Node('foo', pl._header, pl._trailer)
        pl._header._next = n
        pl._trailer._prev = n
        expected_position = PositionalList.Position(pl, n)

        result_position = pl._make_position(n)

        #  comparing the instances done using the Position's __eq__ method
        self.assertEqual(result_position, expected_position)

    def test_first_returns_first_Position_in_the_list(self):
        pl = PositionalList()
        n = PositionalList._Node('foo', pl._header, pl._trailer)
        pl._header._next = n
        pl._trailer._prev = n
        expected_position = PositionalList.Position(pl, n)

        result_position = pl.first()

        self.assertEqual(result_position, expected_position)

    def test_last_returns_last_Position_in_the_list(self):
        pl = PositionalList()
        n = PositionalList._Node('foo', pl._header, pl._trailer)
        pl._header._next = n
        pl._trailer._prev = n
        expected_position = PositionalList.Position(pl, n)

        result_position = pl.last()

        self.assertEqual(result_position, expected_position)

    def test_before_returns_None_with_passed_first_Position_in_list(self):
        pl = PositionalList()
        #  create two nodes with proper references in the container:
        n1 = PositionalList._Node('foo', pl._header, pl._trailer)
        n2 = PositionalList._Node('bar', n1, pl._trailer)
        n1._next = n2
        pl._header._next = n1
        pl._trailer._prev = n2
        #  #  create a position for each respective node:
        p1 = PositionalList.Position(pl, n1)

        result = pl.before(p1)

        self.assertIsNone(result)

    def test_before_returns_Position_before_passed_Position(self):
        pl = PositionalList()
        #  create two nodes with proper references in the container:
        n1 = PositionalList._Node('foo', pl._header, pl._trailer)
        n2 = PositionalList._Node('bar', n1, pl._trailer)
        n1._next = n2
        pl._header._next = n1
        pl._trailer._prev = n2
        #  #  create a position for each respective node:
        p1 = PositionalList.Position(pl, n1)
        p2 = PositionalList.Position(pl, n2)

        result = pl.before(p2)

        self.assertEqual(result, p1)

    def test_after_returns_None_with_passed_last_Position_in_list(self):
        pl = PositionalList()
        #  create two nodes with proper references in the container:
        n1 = PositionalList._Node('foo', pl._header, pl._trailer)
        n2 = PositionalList._Node('bar', n1, pl._trailer)
        n1._next = n2
        pl._header._next = n1
        pl._trailer._prev = n2
        p2 = PositionalList.Position(pl, n2)

        result = pl.after(p2)

        self.assertIsNone(result)

    def test_after_returns_Position_after_passed_Position(self):
        pl = PositionalList()
        #  create two nodes with proper references in the container:
        n1 = PositionalList._Node('foo', pl._header, pl._trailer)
        n2 = PositionalList._Node('bar', n1, pl._trailer)
        n1._next = n2
        pl._header._next = n1
        pl._trailer._prev = n2
        #  #  create a position for each respective node:
        p1 = PositionalList.Position(pl, n1)
        p2 = PositionalList.Position(pl, n2)

        result = pl.after(p1)

        self.assertEqual(result, p2)

    def test_iter_returns_a_forward_generation_of_the_elements_in_the_list(self):
        pl = PositionalList()
        first_element = 'foo'
        second_element = 'bar'
        #  create two nodes with proper references in the container:
        n1 = PositionalList._Node(first_element, pl._header, pl._trailer)
        n2 = PositionalList._Node(second_element, n1, pl._trailer)
        n1._next = n2
        pl._header._next = n1
        pl._trailer._prev = n2

        results = [r for r in pl]

        self.assertIs(results[0], first_element)
        self.assertIs(results[1], second_element)

    def test_add_first_inserts_element_at_front_and_returns_Position(self):
        pl = PositionalList()
        element = 'foo'

        result_position = pl.add_first(element)

        self.assertIs(result_position._node._element, element)
        self.assertIs(result_position._node._prev, pl._header)
        self.assertIs(pl._header._next, result_position._node)

    def test_add_last_inserts_element_at_back_and_returns_Position(self):
        pl = PositionalList()
        element = 'foo'

        result_position = pl.add_last(element)

        self.assertIs(result_position._node._element, element)
        self.assertIs(result_position._node._next, pl._trailer)
        self.assertIs(pl._trailer._prev, result_position._node)

    def test_add_before_inserts_element_before_given_Position_and_returns_Position(self):
        pl = PositionalList()
        n = PositionalList._Node('foo', pl._header, pl._trailer)
        pl._header._next = n
        pl._trailer._prev = n
        existing_position = PositionalList.Position(pl, n)
        element = 'foo'

        result_position = pl.add_before(existing_position, element)

        self.assertIs(result_position._node._element, element)
        self.assertIs(result_position._node._next, existing_position._node)
        self.assertIs(existing_position._node._prev, result_position._node)
        self.assertIs(pl._header._next, result_position._node)

    def test_add_after_inserts_element_after_given_Position_and_returns_Position(self):
        pl = PositionalList()
        n = PositionalList._Node('foo', pl._header, pl._trailer)
        pl._header._next = n
        pl._trailer._prev = n
        existing_position = PositionalList.Position(pl, n)
        element = 'foo'

        result_position = pl.add_after(existing_position, element)

        self.assertIs(result_position._node._element, element)
        self.assertIs(result_position._node._prev, existing_position._node)
        self.assertIs(result_position._node._next, pl._trailer)
        self.assertIs(existing_position._node._next, result_position._node)

    def test_delete_validates_and_calls_delete_node_on_position(self):
        pl = PositionalList()
        expected_element = 'foo'
        node = PositionalList._Node(expected_element, None, None)
        pl._validate = MagicMock(return_value=node)
        pl._delete_node = MagicMock(return_value=expected_element)
        position = PositionalList.Position(pl, node)

        result_element = pl.delete(position)

        pl._validate.assert_called_with(position)
        pl._delete_node.assert_called_with(node)
        self.assertIs(result_element, expected_element)

    def test_replace_validates_replaces_returns_old_element(self):
        pl = PositionalList()
        original_element = 'foo'
        new_element = 'bar'
        node = PositionalList._Node(original_element, None, None)
        pl._validate = MagicMock(return_value=node)
        position = PositionalList.Position(pl, node)

        result_element = pl.replace(position, new_element)

        pl._validate.assert_called_with(position)
        self.assertIs(result_element, original_element)
        self.assertIs(node._element, new_element)
