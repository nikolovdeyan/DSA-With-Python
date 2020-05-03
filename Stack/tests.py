import unittest
from stack import ArrayStack
from empty import Empty


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

    def test_push_adds_an_element_to_stack(self):
        s = ArrayStack()
        expected_element = 'foo'

        s.push(expected_element)

        self.assertIn(expected_element, s._data)

    def test_top_should_return_top_element_without_removing_it(self):
        s = ArrayStack()
        s.push('foo')
        s.push('bar')

        top_element = s.top()

        self.assertEqual(top_element, 'bar')
        self.assertIn('bar', s._data)

    def test_top_should_throw_empty_exception_if_stack_is_empty(self):
        s = ArrayStack()

        self.assertRaises(Empty, s.top)

    def test_pop_should_return_top_element_and_remove_it_from_stack(self):
        s = ArrayStack()
        expected_result = 'baz'
        elements = ['foo', 'bar', expected_result]
        s._data = elements

        result = s.pop()

        self.assertEqual(result, expected_result)
        self.assertNotIn(expected_result, s._data)

    def test_pop_should_throw_empty_exception_if_stack_is_empty(self):
        s = ArrayStack()

        self.assertRaises(Empty, s.top)
