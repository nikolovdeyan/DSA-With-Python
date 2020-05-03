import unittest
from unittest.mock import MagicMock
from singly_linked import LinkedStack, LinkedQueue
from circularly_linked import CircularQueue
from doubly_linked import _DoublyLinkedBase, LinkedDeque, PositionalList
from empty import Empty


class TestLinkedStackMethods(unittest.TestCase):

    def test_len_returns_correct_stack_length(self):
        s = LinkedStack()
        expected_size = 0
        actual_size = len(s)

        self.assertEqual(actual_size, expected_size)

        s._size = 1
        expected_size = 1
        actual_size = len(s)

        self.assertEqual(actual_size, expected_size)

    def test_is_empty_returns_correct_boolean_value(self):
        s = LinkedStack()

        self.assertTrue(s.is_empty())

        s._size = 1

        self.assertFalse(s.is_empty())

    def test_push_should_add_element_to_stack(self):
        s = LinkedStack()

        s.push('foo')

        self.assertIn('foo', s._head._element)

    def test_top_should_return_top_element_without_removing_it(self):
        s = LinkedStack()
        e1 = s._Node('foo', None)
        s._head = e1
        s._size = 1
        expected_result = 'bar'
        e2 = s._Node(expected_result, e1)
        s._head = e2
        s._size = 2

        result = s.top()

        self.assertEqual(result, expected_result)
        self.assertIn(expected_result, s._head._element)

    def test_top_should_throw_empty_exception_if_stack_is_empty(self):
        s = LinkedStack()

        self.assertRaises(Empty, s.top)

    def test_pop_should_return_top_element_and_remove_it_from_stack(self):
        s = LinkedStack()
        e1 = s._Node('foo', None)
        s._head = e1
        s._size = 1
        expected_result = 'bar'
        e2 = s._Node(expected_result, e1)
        s._head = e2
        s._size = 2

        result = s.pop()
        stack_size = s._size

        self.assertEqual(stack_size, 1)
        self.assertEqual(result, expected_result)
        self.assertNotIn(expected_result, s._head._element)

    def test_pop_should_throw_empty_exception_if_stack_is_empty(self):
        s = LinkedStack()

        self.assertRaises(Empty, s.top)


class TestLinkedQueueMethods(unittest.TestCase):

    def test_len_returns_correct_queue_length(self):
        q = LinkedQueue()
        expected_size = 0
        actual_size = len(q)

        self.assertEqual(actual_size, expected_size)

        q._size = 1
        expected_size = 1
        actual_size = len(q)

        self.assertEqual(actual_size, expected_size)

    def test_is_empty_returns_correct_boolean_value(self):
        q = LinkedQueue()

        self.assertTrue(q.is_empty())

        q._size = 1

        self.assertFalse(q.is_empty())

    def test_first_returns_first_element_without_removing_it(self):
        q = LinkedQueue()
        q._head = LinkedQueue._Node('foo', None)
        q._size = 1
        expected_result = 'foo'

        result = q.first()

        self.assertEqual(result, expected_result)
        self.assertIn(expected_result, q._head._element)

    def test_first_raises_empty_exception_if_queue_is_empty(self):
        q = LinkedQueue()

        self.assertRaises(Empty, q.first)

    def test_enqueue_adds_an_element_to_the_back_of_queue(self):
        q = LinkedQueue()
        first_element = LinkedQueue._Node('foo', None)
        q._head = first_element
        q._tail = first_element
        q._size = 1
        second_element = 'bar'

        q.enqueue(second_element)
        result = q._tail._element

        self.assertEqual(result, second_element)

    def test_dequeue_returns_and_removes_first_element_from_queue(self):
        q = LinkedQueue()
        second_element = LinkedQueue._Node('bar', None)
        first_element = LinkedQueue._Node('foo', second_element)
        q._head = first_element
        q._tail = second_element
        q._size = 2
        expected_result = 'foo'

        result = q.dequeue()

        self.assertEqual(q._size, 1)
        self.assertEqual(result, expected_result)
        self.assertIsNot(q._head, first_element)

    def test_dequeue_raises_empty_exception_if_queue_is_empty(self):
        q = LinkedQueue()

        self.assertRaises(Empty, q.dequeue)


class TestCircularQueueMethods(unittest.TestCase):

    def test_len_returns_correct_queue_length(self):
        q = CircularQueue()
        expected_size = 0
        actual_size = len(q)

        self.assertEqual(actual_size, expected_size)

        q._size = 1
        expected_size = 1
        actual_size = len(q)

        self.assertEqual(actual_size, expected_size)

    def test_is_empty_returns_correct_boolean_value(self):
        q = CircularQueue()

        self.assertTrue(q.is_empty())

        q._size = 1

        self.assertFalse(q.is_empty())

    def test_first_returns_first_element_without_removing_it(self):
        q = CircularQueue()
        newest = CircularQueue._Node('foo', None)
        newest._next = newest
        q._tail = newest
        q._size = 1
        expected_result = 'foo'

        result = q.first()

        self.assertEqual(result, expected_result)
        self.assertIn(expected_result, q._tail._next._element)

    def test_first_raises_empty_exception_if_queue_is_empty(self):
        q = CircularQueue()

        self.assertRaises(Empty, q.first)

    def test_enqueue_adds_an_element_to_the_back_of_queue(self):
        q = CircularQueue()
        first_element = CircularQueue._Node('foo', None)
        first_element._next = first_element
        q._tail = first_element
        q._size = 1
        second_element = 'bar'

        q.enqueue(second_element)
        result = q._tail._element

        self.assertEqual(result, second_element)

    def test_dequeue_returns_and_removes_first_element_from_queue(self):
        q = CircularQueue()
        second_element = CircularQueue._Node('bar', None)
        first_element = CircularQueue._Node('foo', None)
        q._tail = second_element
        q._tail._next = first_element
        q._size = 2
        expected_result = 'foo'

        result = q.dequeue()

        self.assertEqual(q._size, 1)
        self.assertEqual(result, expected_result)
        self.assertIsNot(q._tail._next, first_element)

    def test_dequeue_raises_empty_exception_if_queue_is_empty(self):
        q = CircularQueue()

        self.assertRaises(Empty, q.dequeue)

    def test_rotate_moves_front_element_to_back_of_queue(self):
        q = CircularQueue()
        second_element = CircularQueue._Node('bar', None)
        first_element = CircularQueue._Node('foo', None)
        q._tail = second_element
        q._tail._next = first_element
        q._size = 2
        expected_result = 'foo'

        q.rotate()
        result = q._tail._element

        self.assertEqual(result, expected_result)


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


class TestLinkedDequeMethods(unittest.TestCase):

    def test_first_raises_empty_exception_if_deque_is_empty(self):
        d = LinkedDeque()

        self.assertRaises(Empty, d.first)

    def test_first_returns_first_element_without_removing_it(self):
        d = LinkedDeque()
        expected_element = 'foo'
        #  add first element
        n1 = LinkedDeque._Node(expected_element, d._header, d._trailer)
        d._header._next = n1
        d._trailer._prev = n1
        d._size = 1
        #  add second element
        n2 = LinkedDeque._Node('bar', n1, d._trailer)
        n1._next = n2
        d._trailer._prev = n2
        d._size = 2

        returned_element = d.first()

        #  check the return element:
        self.assertIs(returned_element, expected_element)
        #  check size of the deque has not changed:
        self.assertEqual(d._size, 2)

    def test_last_raises_empty_exception_if_deque_is_empty(self):
        d = LinkedDeque()

        self.assertRaises(Empty, d.last)

    def test_last_returns_last_element_without_removing_it(self):
        d = LinkedDeque()
        expected_element = 'bar'
        #  add first element
        n1 = LinkedDeque._Node('foo', d._header, d._trailer)
        d._header._next = n1
        d._trailer._prev = n1
        d._size = 1
        #  add second element
        n2 = LinkedDeque._Node(expected_element, n1, d._trailer)
        n1._next = n2
        d._trailer._prev = n2
        d._size = 2

        returned_element = d.last()

        #  check the return element:
        self.assertIs(returned_element, expected_element)
        #  check size of the deque has not changed:
        self.assertEqual(d._size, 2)

    def test_insert_first_adds_an_element_to_the_front_of_the_deque(self):
        d = LinkedDeque()
        expected_element = 'foo'

        d.insert_first(expected_element)

        exp_element_node = d._header._next
        self.assertIs(d._header._next._element, expected_element)
        self.assertIs(exp_element_node._next, d._trailer)

    def test_insert_last_adds_an_element_to_the_back_of_the_deque(self):
        d = LinkedDeque()
        expected_element = 'foo'

        d.insert_last(expected_element)

        exp_element_node = d._trailer._prev
        self.assertIs(d._trailer._prev._element, expected_element)
        self.assertIs(exp_element_node._prev, d._header)

    def test_delete_first_raises_empty_exception_if_deque_is_empty(self):
        d = LinkedDeque()

        self.assertRaises(Empty, d.delete_first)

    def test_delete_first_returns_and_removes_from_the_front_of_the_deque(self):
        d = LinkedDeque()
        expected_element = 'foo'
        #  add first element
        n1 = LinkedDeque._Node(expected_element, d._header, d._trailer)
        d._header._next = n1
        d._trailer._prev = n1
        d._size = 1
        #  add second element
        n2 = LinkedDeque._Node('bar', n1, d._trailer)
        n1._next = n2
        d._trailer._prev = n2
        d._size = 2

        deleted_element = d.delete_first()

        #  check the return element:
        self.assertIs(deleted_element, expected_element)
        #  check size of the deque is updated:
        self.assertEqual(d._size, 1)

    def test_delete_last_raises_empty_exception_if_deque_is_empty(self):
        d = LinkedDeque()

        self.assertRaises(Empty, d.delete_last)

    def test_delete_last_returns_and_removes_from_the_front_of_the_deque(self):
        d = LinkedDeque()
        expected_element = 'bar'
        #  add first element
        n1 = LinkedDeque._Node('foo', d._header, d._trailer)
        d._header._next = n1
        d._trailer._prev = n1
        d._size = 1
        #  add second element
        n2 = LinkedDeque._Node(expected_element, n1, d._trailer)
        n1._next = n2
        d._trailer._prev = n2
        d._size = 2

        deleted_element = d.delete_last()

        #  check the return element:
        self.assertIs(deleted_element, expected_element)
        #  check size of the deque is updated:
        self.assertEqual(d._size, 1)


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
