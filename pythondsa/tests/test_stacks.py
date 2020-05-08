import unittest
from pythondsa.src.stacks import ArrayStack, LinkedStack
from pythondsa.src.exceptions import Empty, Full


class TestArrayStackMethods(unittest.TestCase):

    def test_len_returns_size_of_stack(self):
        s = ArrayStack()
        expected_result = 0

        result = len(s)

        self.assertEqual(result, expected_result)

        elements = ['foo', 'bar', 'baz']
        s._data = elements
        expected_result = 3

        result = len(s)

        self.assertEqual(result, expected_result)

    def test_is_empty_returns_correct_boolean_value(self):
        s = ArrayStack()

        self.assertTrue(s.is_empty())

        s._data = ['foo']

        self.assertFalse(s.is_empty())

    def test_is_full_returns_correct_boolean_value(self):
        s = ArrayStack()

        self.assertFalse(s.is_full())

        s._data = ['foo', 'bar']
        s._maxlen = 2

        self.assertTrue(s.is_full())

    def test_push_adds_an_element_to_stack(self):
        s = ArrayStack()
        expected_element = 'foo'

        s.push(expected_element)

        self.assertIn(expected_element, s._data)

    def test_push_raises_full_exception_with_full_stack(self):
        s = ArrayStack(maxlen=2)
        s._data = ['foo', 'bar']

        self.assertRaises(Full, s.push, 'baz')

    def test_top_returns_top_element_without_removing_it(self):
        s = ArrayStack()
        s.push('foo')
        s.push('bar')

        top_element = s.top()

        self.assertEqual(top_element, 'bar')
        self.assertIn('bar', s._data)

    def test_top_raises_empty_exception_if_stack_is_empty(self):
        s = ArrayStack()

        self.assertRaises(Empty, s.top)

    def test_pop_returns_top_element_and_remove_it_from_stack(self):
        s = ArrayStack()
        expected_result = 'baz'
        elements = ['foo', 'bar', expected_result]
        s._data = elements

        result = s.pop()

        self.assertEqual(result, expected_result)
        self.assertNotIn(expected_result, s._data)

    def test_pop_raises_empty_exception_if_stack_is_empty(self):
        s = ArrayStack()

        self.assertRaises(Empty, s.top)


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
