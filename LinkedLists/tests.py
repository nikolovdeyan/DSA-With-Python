import unittest
from singly_linked import LinkedStack, LinkedQueue
from empty import Empty


class TestLinkedStackMethods(unittest.TestCase):

    def test_constructor_creates_an_empty_stack(self):
        s = LinkedStack()

        self.assertIsInstance(s, LinkedStack)

    def test_empty_stack_size_should_be_zero(self):
        s = LinkedStack()
        expected_size = 0
        actual_size = s._size

        self.assertEqual(actual_size, expected_size)

    def test_len_should_return_size_of_stack(self):
        s0 = LinkedStack()      # Empty stack

        s1 = LinkedStack()
        s1.push('foo')    # LinkedStack with 1 element

        s2 = LinkedStack()
        s2.push('foo')
        s2.push('foo')    # LinkedStack with 2 elements

        self.assertEqual(len(s0), 0)
        self.assertEqual(len(s1), 1)
        self.assertEqual(len(s2), 2)

    def test_is_empty_should_return_true_if_stack_is_empty(self):
        s = LinkedStack()

        self.assertTrue(s.is_empty())

    def test_push_should_add_element_to_stack(self):
        s = LinkedStack()

        s.push('foo')

        self.assertIn('foo', s._head._element)

    def test_top_should_return_top_element_without_removing_it(self):
        s = LinkedStack()
        s.push('foo')
        s.push('bar')

        top_element = s.top()

        self.assertEqual(top_element, 'bar')
        self.assertIn('bar', s._head._element)

    def test_top_should_throw_empty_exception_if_stack_is_empty(self):
        s = LinkedStack()

        self.assertRaises(Empty, s.top)

    def test_pop_should_return_top_element_and_remove_it_from_stack(self):
        s = LinkedStack()
        s.push('foo')
        s.push('bar')

        popped_element = s.pop()
        stack_size = s._size

        self.assertEqual(stack_size, 1)
        self.assertEqual(popped_element, 'bar')
        self.assertNotIn('bar', s._head._element)

    def test_pop_should_throw_empty_exception_if_stack_is_empty(self):
        s = LinkedStack()

        self.assertRaises(Empty, s.top)


class TestLinkedQueueMethods(unittest.TestCase):

    def test_constructor_creates_an_empty_queue(self):
        q = LinkedQueue()

        self.assertIsInstance(q, LinkedQueue)

    def test_empty_queue_size_is_zero(self):
        q = LinkedQueue()
        expected_size = 0
        actual_size = q._size

        self.assertEqual(actual_size, expected_size)

    def test_is_empty_returns_true_if_queue_is_empty(self):
        q = LinkedQueue()

        self.assertTrue(q.is_empty)

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

