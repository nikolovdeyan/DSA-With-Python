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

    def test_first_raises_empty_exception_if_queue_is_empty(self):
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

    def test_dequeue_raises_empty_exception_if_queue_is_empty(self):
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


class TestArrayDequeMethods(unittest.TestCase):
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

    def test_is_empty_returns_correct_boolean_value(self):
        d = ArrayDeque()

        self.assertTrue(d.is_empty())

        elements = ['foo', 'bar', 'baz']
        d._data[2:5] = elements
        d._size = 3
        d._front = 2

        self.assertFalse(d.is_empty())

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

    def test_first_raises_empty_exception_if_deque_is_empty(self):
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

    def test_last_raises_empty_exception_if_deque_is_empty(self):
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

    def test_delete_first_raises_empty_exception_if_deque_is_empty(self):
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

    def test_delete_last_raises_empty_exception_if_deque_is_empty(self):
        d = ArrayDeque()

        self.assertRaises(Empty, d.delete_last)


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
