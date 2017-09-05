import unittest
from stack import Stack
from empty import Empty


class TestStackMethods(unittest.TestCase):

    def test_constructor_creates_an_empty_stack(self):
        s = Stack()

        self.assertIsInstance(s, Stack)

    def test_empty_stack_size_should_be_zero(self):
        s = Stack()
        expected_size = 0

        actual_size = len(s._data)

        self.assertEqual(actual_size, expected_size)

    def test_len_should_return_size_of_stack(self):
        s0 = Stack()      # Empty stack

        s1 = Stack()
        s1.push('foo')    # Stack with 1 element

        s2 = Stack()
        s2.push('foo')
        s2.push('foo')    # Stack with 2 elements

        self.assertEqual(len(s0), 0)
        self.assertEqual(len(s1), 1)
        self.assertEqual(len(s2), 2)

    def test_is_empty_should_return_true_if_stack_is_empty(self):
        s = Stack()

        self.assertTrue(s.is_empty())

    def test_push_should_add_element_to_stack(self):
        s = Stack()

        s.push('foo')

        self.assertIn('foo', s._data)

    def test_top_should_return_top_element_without_removing_it(self):
        s = Stack()
        s.push('foo')
        s.push('bar')

        top_element = s.top()

        self.assertEqual(top_element, 'bar')
        self.assertIn('bar', s._data)

    def test_top_should_throw_empty_exception_if_stack_is_empty(self):
        s = Stack()

        self.assertRaises(Empty, s.top)

    def test_pop_should_return_top_element_and_remove_it_from_stack(self):
        s = Stack()
        s.push('foo')
        s.push('bar')

        popped_element = s.pop()
        stack_size = len(s._data)

        self.assertEqual(stack_size, 1)
        self.assertEqual(popped_element, 'bar')
        self.assertNotIn('bar', s._data)

    def test_pop_should_throw_empty_exception_if_stack_is_empty(self):
        s = Stack()

        self.assertRaises(Empty, s.top)
