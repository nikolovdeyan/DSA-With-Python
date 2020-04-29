import unittest
from queues import ArrayQueue, ArrayDeque
from empty import Empty


class TestArrayQueueMethods(unittest.TestCase):

    def test_constructor_creates_an_queue(self):
        q = ArrayQueue()

        self.assertIsInstance(q, ArrayQueue)

    def test_empty_queue_size(self):
        q = ArrayQueue()
        expected_size = ArrayQueue.DEFAULT_CAPACITY

        actual_size = len(q._data)

        self.assertEqual(actual_size, expected_size)

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

    def test_is_empty_returns_true_if_queue_is_empty(self):
        q = ArrayQueue()

        self.assertTrue(q.is_empty())

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


class TestArrayDequeMethods(unittest.TestCase):
    def test_constructor_creates_ArrayDeque(self):
        d = ArrayDeque()

        self.assertIsInstance(d, ArrayDeque)

    def test_empty_deque_size(self):
        d = ArrayDeque()
        expected_size = ArrayDeque.DEFAULT_CAPACITY

        actual_size = len(d._data)

        self.assertEqual(actual_size, expected_size)

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

    def test_is_empty_returns_true_if_deque_is_empty(self):
        d = ArrayDeque()

        self.assertTrue(d.is_empty())

    def test_is_empty_returns_false_if_deque_is_not_empty(self):
        elements = ['foo', 'bar', 'baz']
        d = ArrayDeque()
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
