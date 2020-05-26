import unittest
from pythondsa.src.queues import ArrayQueue, ArrayDeque, LinkedDeque
from pythondsa.src.queues import LinkedQueue, CircularQueue
from pythondsa.src.exceptions import Empty


class TestArrayQueueMethods(unittest.TestCase):

    def test_len_returns_size_of_queue(self):
        q = ArrayQueue()
        expected_result = 0

        result = len(q)

        self.assertEqual(result, expected_result)

        q._data = ['foo']
        q._size = 1
        expected_result = 1

        result = len(q)

        self.assertEqual(result, expected_result)

    def test_resize_increases_capacity(self):
        q = ArrayQueue()

        q._resize(50)

        self.assertEqual(len(q._data), 50)

    def test_resize_preserves_order_of_enqueued_elements(self):
        elements = ['foo', 'bar', 'baz']
        expected_sequence = [None] * 20
        expected_sequence[0:3] = elements
        q = ArrayQueue()
        q._data[2:5] = elements
        q._size = 3
        q._front = 2

        q._resize(20)

        self.assertSequenceEqual(q._data, expected_sequence)

    def test_is_empty_returns_correct_boolean_value(self):
        q = ArrayQueue()

        self.assertTrue(q.is_empty())

        q._data = ['foo']
        q._size = 1

        self.assertFalse(q.is_empty())

    def test_first_returns_first_element_without_removing_it(self):
        elements = ['foo', 'bar', 'baz']
        expected_result = 'foo'
        q = ArrayQueue()
        q._data[2:5] = elements
        q._size = 3
        q._front = 2

        result = q.first()

        self.assertEqual(result, expected_result)
        self.assertIn(expected_result, q._data)

    def test_first_raises_Empty_exception_if_queue_is_empty(self):
        q = ArrayQueue()

        self.assertRaises(Empty, q.first)

    def test_enqueue_adds_an_element_to_the_back_of_queue(self):
        elements = ['foo', 'bar']
        expected_result = 'baz'
        q = ArrayQueue()
        q._data[2:4] = elements
        q._size = 2
        q._front = 2

        q.enqueue(expected_result)
        result = q._data[4]

        self.assertEqual(result, expected_result)

    def test_enqueue_doubles_queue_size_if_capacity_reached(self):
        expected_result = ArrayQueue.DEFAULT_CAPACITY * 2
        q = ArrayQueue()

        for e in range(ArrayQueue.DEFAULT_CAPACITY + 1):
            q.enqueue(e)
        result = len(q._data)

        self.assertEqual(result, expected_result)

    def test_dequeue_returns_and_removes_first_element_from_queue(self):
        elements = ['foo', 'bar']
        expected_result = 'foo'
        q = ArrayQueue()
        q._data[2:4] = elements
        q._size = 2
        q._front = 2

        result = q.dequeue()

        self.assertEqual(q._size, 1)
        self.assertEqual(result, expected_result)
        self.assertNotIn('foo', q._data)

    def test_dequeue_raises_Empty_exception_if_queue_is_empty(self):
        q = ArrayQueue()

        self.assertRaises(Empty, q.dequeue)


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

    def test_first_raises_Empty_exception_if_queue_is_empty(self):
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

    def test_dequeue_raises_Empty_exception_if_queue_is_empty(self):
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

    def test_first_raises_Empty_exception_if_queue_is_empty(self):
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

    def test_dequeue_raises_Empty_exception_if_queue_is_empty(self):
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


class TestArrayDequeMethods(unittest.TestCase):

    def test_constructor_with_maxlen_less_than_default_capacity_shrinks_size(self):
        expected_result = 5

        d = ArrayDeque(maxlen=expected_result)  # less than DEFAULT_CAPACITY
        result = len(d._data)

        self.assertEqual(result, expected_result)

    def test_len_returns_size_of_deque(self):
        d = ArrayDeque()
        expected_result = 0

        result = len(d)

        self.assertEqual(result, expected_result)

        d._data = ['foo']
        d._size = 1
        expected_result = 1

        result = len(d)

        self.assertEqual(result, expected_result)

    def test_getitem_raises_IndexError_with_integer_index_out_of_range(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        self.assertRaises(IndexError, d.__getitem__, 3)
        self.assertRaises(IndexError, d.__getitem__, -4)

    def test_getitem_raises_NotImplementedError_with_slice_object_parameter(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz', 'spam', 'eggs']
        d._data[2:7] = elements
        d._front = 2
        d._size = 5

        self.assertRaises(NotImplementedError, d.__getitem__, slice(0, 2))

    def test_getitem_returns_correct_element_with_positive_integer_index(self):
        d = ArrayDeque()
        expected_result = 'foo'
        elements = [expected_result, 'bar', 'baz']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        result = d[0]

        self.assertEqual(result, expected_result)

    def test_getitem_returns_correct_element_with_negative_integer_index(self):
        d = ArrayDeque()
        expected_result = 'foo'
        elements = [expected_result, 'bar', 'baz']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        result = d[-3]

        self.assertEqual(result, expected_result)

    def test_setitem_raises_IndexError_with_integer_index_out_of_range(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        self.assertRaises(IndexError, d.__setitem__, 3, 'nope')
        self.assertRaises(IndexError, d.__setitem__, -4, 'nope')

    def test_setitem_raises_NotImplementedError_with_slice_object_parameter(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz', 'spam', 'eggs']
        d._data[2:7] = elements
        d._front = 2
        d._size = 5

        self.assertRaises(NotImplementedError, d.__setitem__, slice(1, 3), ['zap', 'tap'])

    def test_setitem_replaces_correct_element_with_positive_integer_index(self):
        d = ArrayDeque()
        expected_result = 'spam'
        elements = ['foo', 'bar', 'baz']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        d[0] = expected_result
        result = d[0]

        self.assertEqual(result, expected_result)

    def test_setitem_replaces_correct_element_with_negative_integer_index(self):
        d = ArrayDeque()
        expected_result = 'spam'
        elements = ['foo', 'bar', 'baz']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        d[-3] = expected_result
        result = d[-3]

        self.assertEqual(result, expected_result)

    def test_clear_resets_deque_resizes_data_to_default_capacity_without_maxlen(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        d.clear()

        self.assertEqual(d._size, 0)
        self.assertEqual(d._front, 0)
        self.assertEqual(len(d._data), d.DEFAULT_CAPACITY)

    def test_clear_resets_deque_resizes_data_to_maxlen_with_maxlen_provided(self):
        d = ArrayDeque(maxlen=5)
        elements = ['foo', 'bar', 'baz']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        d.clear()

        self.assertEqual(d._size, 0)
        self.assertEqual(d._front, 0)
        self.assertEqual(len(d._data), d._maxlen)

    def test_rotate_shifts_deque_to_right_with_positive_steps_integer(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz']
        expected_elements = ['bar', 'baz', 'foo']
        d._data[2:5] = elements
        d._front = 2
        d._size = 3

        d.rotate(2)

        self.assertEqual(d._data[0:3], expected_elements)

    def test_rotate_shifts_deque_to_left_with_negative_steps_integer(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz']
        expected_elements = ['baz', 'foo', 'bar']
        d._data[0:3] = elements
        d._front = 0
        d._size = 3

        d.rotate(-2)

        self.assertEqual(d._data[2:5], expected_elements)

    def test_resize_increases_capacity(self):
        d = ArrayDeque()

        d._resize(50)

        self.assertEqual(len(d._data), 50)

    def test_resize_preserves_order_of_enqueued_elements(self):
        elements = ['foo', 'bar', 'baz']
        expected_sequence = [None] * 20
        expected_sequence[0:3] = elements
        d = ArrayDeque()
        d._data[2:5] = elements
        d._size = 3
        d._front = 2

        d._resize(20)

        self.assertSequenceEqual(d._data, expected_sequence)

    def test_remove_deletes_first_instance_of_value_in_deque(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz', 'bar']
        d._data[2:6] = elements
        d._size = 4
        d._front = 2

        d.remove('bar')

        self.assertEqual(d._size, 3)
        self.assertIn('bar', d._data)
        self.assertEqual(d._data[3:6], ['foo', 'baz', 'bar'])

    def test_remove_shifts_elements_from_shorter_end_of_deque(self):
        d = ArrayDeque()
        elements = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th']
        d._data[0:7] = elements
        d._front = 0
        d._size = 7

        # ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th']
        #    0      1      2      3      4      5      6
        # for i in range self._size -> i in range(7):
        # current = 1
        # 1 < self._size // 2 -> 1 < 3
        #

        d.remove('2nd')

        self.assertEqual(d._data[1:7], ['1st', '3rd', '4th', '5th', '6th', '7th'])
        self.assertEqual(d._front, 1)  # front moved as elements left of center shifted

        d.remove('6th')

        self.assertEqual(d._data[1:6], ['1st', '3rd', '4th', '5th', '7th'])
        self.assertEqual(d._front, 1)  # the front has not moved

    def test_remove_raises_ValueError_when_value_not_in_deque(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz', 'bar']
        d._data[2:6] = elements
        d._size = 4
        d._front = 2

        self.assertRaises(ValueError, d.remove, 'spam')

    def test_count_returns_correct_number_of_matches_for_value_in_deque(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz', 'bar']
        d._data[-2:2] = elements
        d._size = 4
        d._front = 8

        self.assertEqual(2, d.count('bar'))
        self.assertEqual(1, d.count('foo'))
        self.assertEqual(0, d.count('spam'))

    def test_is_empty_returns_correct_boolean_value(self):
        d = ArrayDeque()

        self.assertTrue(d.is_empty())

        elements = ['foo', 'bar', 'baz']
        d._data[2:5] = elements
        d._size = 3
        d._front = 2

        self.assertFalse(d.is_empty())

    def test_is_full_returns_correct_boolean_value(self):
        d = ArrayDeque()
        elements = ['foo', 'bar', 'baz', 'spam', 'eggs']
        d._data[2:7] = elements
        d._size = 5
        d._front = 2

        self.assertFalse(d.is_full())

        d = ArrayDeque(maxlen=5)
        elements = ['foo', 'bar', 'baz', 'spam', 'eggs']
        d._data = elements
        d._size = 5

        self.assertTrue(d.is_full())

    def test_first_returns_first_element_without_removing_it(self):
        elements = ['foo', 'bar', 'baz']
        expected_result = 'foo'
        d = ArrayDeque()
        d._data[2:5] = elements
        d._size = 3
        d._front = 2

        result = d.first()

        self.assertEqual(result, expected_result)
        self.assertIn(expected_result, d._data)

    def test_first_raises_Empty_exception_if_deque_is_empty(self):
        d = ArrayDeque()

        self.assertRaises(Empty, d.first)

    def test_last_returns_last_element_without_removing_it(self):
        elements = ['foo', 'bar', 'baz']
        expected_result = 'baz'
        d = ArrayDeque()
        d._data[2:5] = elements
        d._size = 3
        d._front = 2

        result = d.last()

        self.assertEqual(result, expected_result)
        self.assertIn(expected_result, d._data)

    def test_last_raises_Empty_exception_if_deque_is_empty(self):
        d = ArrayDeque()

        self.assertRaises(Empty, d.last)

    def test_add_first_adds_an_element_to_the_front_of_deque(self):
        elements = ['bar', 'baz']
        expected_result = 'foo'
        d = ArrayDeque()
        d._data[2:4] = elements
        d._size = 2
        d._front = 2

        d.add_first(expected_result)
        result = d._data[1]

        self.assertEqual(result, expected_result)

    def test_add_first_doubles_deque_size_if_capacity_reached(self):
        expected_result = ArrayDeque.DEFAULT_CAPACITY * 2
        d = ArrayDeque()

        for e in range(ArrayDeque.DEFAULT_CAPACITY + 1):
            d.add_first(e)
        result = len(d._data)

        self.assertEqual(result, expected_result)

    def test_add_last_doubles_deque_size_if_capacity_reached(self):
        expected_result = ArrayDeque.DEFAULT_CAPACITY * 2
        d = ArrayDeque()

        for e in range(ArrayDeque.DEFAULT_CAPACITY + 1):
            d.add_last(e)
        result = len(d._data)

        self.assertEqual(result, expected_result)

    def test_add_last_adds_an_element_to_the_back_of_deque(self):
        elements = ['foo', 'bar']
        expected_result = 'baz'
        d = ArrayDeque()
        d._data[2:4] = elements
        d._size = 2
        d._front = 2

        d.add_last(expected_result)
        result = d._data[4]

        self.assertEqual(result, expected_result)

    def test_delete_first_returns_and_removes_first_element_from_deque(self):
        elements = ['foo', 'bar']
        expected_result = 'foo'
        d = ArrayDeque()
        d._data[2:4] = elements
        d._size = 2
        d._front = 2

        result = d.delete_first()

        self.assertEqual(d._size, 1)
        self.assertEqual(result, expected_result)
        self.assertNotIn('foo', d._data)

    def test_delete_first_raises_Empty_exception_if_deque_is_empty(self):
        d = ArrayDeque()

        self.assertRaises(Empty, d.delete_first)

    def test_delete_last_returns_and_removes_last_element_from_deque(self):
        elements = ['foo', 'bar']
        expected_result = 'bar'
        d = ArrayDeque()
        d._data[2:4] = elements
        d._size = 2
        d._front = 2

        result = d.delete_last()

        self.assertEqual(d._size, 1)
        self.assertEqual(result, expected_result)
        self.assertNotIn('bar', d._data)

    def test_delete_last_raises_Empty_exception_if_deque_is_empty(self):
        d = ArrayDeque()

        self.assertRaises(Empty, d.delete_last)


class TestLinkedDequeMethods(unittest.TestCase):

    def test_first_raises_Empty_exception_if_deque_is_empty(self):
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

    def test_last_raises_Empty_exception_if_deque_is_empty(self):
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

    def test_delete_first_raises_Empty_exception_if_deque_is_empty(self):
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

    def test_delete_last_raises_Empty_exception_if_deque_is_empty(self):
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
