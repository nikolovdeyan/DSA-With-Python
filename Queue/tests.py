import unittest
from queue import Queue
from empty import Empty


class TestQueueMethods(unittest.TestCase):

    def test_constructor_creates_an_empty_queue(self):
        q = Queue()

        self.assertIsInstance(q, Queue)

    def test_empty_queue_size_is_zero(self):
        q = Queue()
        expected_size = Queue.DEFAULT_CAPACITY

        actual_size = len(q._data)

        self.assertEqual(actual_size, expected_size)

    def test_resize_increases_capacity(self):
        q = Queue()

        q._resize(50)

        self.assertEqual(len(q._data), 50)

    def test_resize_preserves_order_of_enqueued_elements(self):
        elements = ['foo', 'bar', 'baz']
        expected_sequence = [None] * 20
        expected_sequence[0:3] = elements
        q = Queue()
        q._data[2:5] = elements
        q._size = 3
        q._front = 2

        q._resize(20)

        self.assertSequenceEqual(q._data, expected_sequence)

    def test_is_empty_returns_true_if_queue_is_empty(self):
        q = Queue()

        self.assertTrue(q.is_empty)

    def test_first_returns_first_element_without_removing_it(self):
        elements = ['foo', 'bar', 'baz']
        expected_result = 'foo'
        q = Queue()
        q._data[2:5] = elements
        q._size = 3
        q._front = 2

        result = q.first()

        self.assertEqual(result, expected_result)
        self.assertIn(expected_result, q._data)

    def test_first_raises_empty_exception_if_queue_is_empty(self):
        q = Queue()

        self.assertRaises(Empty, q.first)

    def test_enqueue_adds_an_element_to_the_back_of_queue(self):
        elements = ['foo', 'bar']
        expected_result = 'baz'
        q = Queue()
        q._data[2:4] = elements
        q._size = 2
        q._front = 2

        q.enqueue(expected_result)
        result = q._data[4]

        self.assertEqual(result, expected_result)

    def test_enqueue_doubles_queue_size_if_capacity_reached(self):
        expected_result = Queue.DEFAULT_CAPACITY * 2
        q = Queue()

        for e in range(Queue.DEFAULT_CAPACITY + 1):
            q.enqueue(e)
        result = len(q._data)

        self.assertEqual(result, expected_result)

    def test_dequeue_returns_and_removes_first_element_from_queue(self):
        elements = ['foo', 'bar']
        expected_result = 'foo'
        q = Queue()
        q._data[2:4] = elements
        q._size = 2
        q._front = 2

        result = q.dequeue()

        self.assertEqual(q._size, 1)
        self.assertEqual(result, expected_result)
        self.assertNotIn('foo', q._data)

    def test_dequeue_raises_empty_exception_if_queue_is_empty(self):
        q = Queue()

        self.assertRaises(Empty, q.dequeue)
