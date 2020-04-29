import unittest
from stack import ArrayStack
from empty import Empty


class TestArrayStackMethods(unittest.TestCase):

    def test_constructor_creates_an_empty_stack(self):
        s = ArrayStack()

        self.assertIsInstance(s, ArrayStack)

    def test_empty_stack_size_should_be_zero(self):
        s = ArrayStack()
        expected_size = 0

        actual_size = len(s._data)

        self.assertEqual(actual_size, expected_size)

    def test_len_should_return_size_of_stack(self):
        s0 = ArrayStack()      # Empty stack

        s1 = ArrayStack()
        s1.push('foo')    # Stack with 1 element

        s2 = ArrayStack()
        s2.push('foo')
        s2.push('foo')    # Stack with 2 elements

        self.assertEqual(len(s0), 0)
        self.assertEqual(len(s1), 1)
        self.assertEqual(len(s2), 2)

    def test_is_empty_should_return_true_if_stack_is_empty(self):
        s = ArrayStack()

        self.assertTrue(s.is_empty())

    def test_push_should_add_element_to_stack(self):
        s = ArrayStack()

        s.push('foo')

        self.assertIn('foo', s._data)

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
        s.push('foo')
        s.push('bar')

        popped_element = s.pop()
        stack_size = len(s._data)

        self.assertEqual(stack_size, 1)
        self.assertEqual(popped_element, 'bar')
        self.assertNotIn('bar', s._data)

    def test_pop_should_throw_empty_exception_if_stack_is_empty(self):
        s = ArrayStack()

        self.assertRaises(Empty, s.top)
