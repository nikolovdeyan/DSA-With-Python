import unittest
from pythondsa.src.arrays import DynamicArray
from pythondsa.src.exceptions import Empty


class TestDynamicArrayMethods(unittest.TestCase):

    def test_len_returns_the_size_of_the_array(self):
        da = DynamicArray()
        expected_result = 0

        result = len(da)

        self.assertEqual(result, expected_result)

        expected_result = 1
        da._n = 1

        result = len(da)

        self.assertEqual(result, expected_result)

    def test_getitem_raises_IndexError_with_invalid_index(self):
        da = DynamicArray()

        self.assertRaises(IndexError, da.__getitem__, 0)

    def test_getitem_returns_correct_element_at_positive_index(self):
        expected_result = 'bar'
        elements = ['foo', expected_result, 'baz']
        da = DynamicArray()
        da._n = 3
        da._capacity = 4
        da._A = da._make_array(da._capacity)
        da._A[0:3] = elements

        result = da[1]

        self.assertEqual(result, expected_result)

    def test_getitem_returns_correct_element_at_negative_index(self):
        elements = ['foo', 'bar', 'baz']
        da = DynamicArray()
        da._capacity = 4
        da._n = 3
        da._A = da._make_array(da._capacity)
        da._A[0:3] = elements

        expected_result = 'baz'
        result = da[-1]
        self.assertEqual(result, expected_result)

        expected_result = 'bar'
        result = da[-2]
        self.assertEqual(result, expected_result)

        expected_result = 'foo'
        result = da[-3]
        self.assertEqual(result, expected_result)

    def test_append_doubles_array_capacity_if_capacity_reached(self):
        da = DynamicArray()
        da._n = 2
        da._capacity = 2
        da._A = da._make_array(da._capacity)
        da._A[0:2] = ['foo', 'bar']
        expected_result = 4

        da.append('spam')
        result = da._capacity

        self.assertEqual(result, expected_result)

    def test_append_adds_object_at_end_of_array(self):
        da = DynamicArray()
        expected_result = 'foo'

        da.append(expected_result)

        self.assertEqual(da._A[-1], expected_result)
        self.assertEqual(da._n, 1)

        expected_result = 'bar'
        da.append(expected_result)

        self.assertEqual(da._A[-1], expected_result)
        self.assertEqual(da._n, 2)

    def test_insert_doubles_array_capacity_if_capacity_reached(self):
        da = DynamicArray()
        da._n = 2
        da._capacity = 2
        da._A = da._make_array(da._capacity)
        da._A[0:2] = ['foo', 'bar']
        expected_result = 4

        da.insert(0, 'spam')
        result = da._capacity

        self.assertEqual(result, expected_result)

    def test_insert_adds_at_index_shifts_items_rightward_with_positive_index(self):
        da = DynamicArray()
        da._n = 3
        da._capacity = 4
        da._A = da._make_array(da._capacity)
        elements = ['foo', 'bar', 'baz']
        da._A[0:3] = elements
        expected_elements = ['foo', 'spam', 'bar', 'baz']

        da.insert(1, 'spam')

        self.assertEqual(da._A[0:5], expected_elements)

    def test_remove_raises_ValueError_with_value_missing_in_array(self):
        da = DynamicArray()
        da._n = 2
        da._capacity = 2
        da._A = da._make_array(da._capacity)
        da._A[0:2] = ['foo', 'bar']

        self.assertRaises(ValueError, da.remove, 'spam')

    def test_remove_removes_first_occurence_of_value_in_array(self):
        da = DynamicArray()
        da._n = 5
        da._capacity = 5
        da._A = da._make_array(da._capacity)
        da._A[0:5] = ['foo', 'bar', 'spam', 'baz', 'spam']
        expected_elements = ['foo', 'bar', 'baz', 'spam']

        da.remove('spam')

        self.assertEqual(da._A[0:4], expected_elements)
        self.assertEqual(da._n, 4)

    def test_remove_halves_array_capacity_if_less_than_quarter_of_capacity_used(self):
        da = DynamicArray()
        da._capacity = 64
        da._n = 17
        da._A = da._make_array(da._capacity)
        da._A[0:17] = [l for l in 'abcdefghijklmnopq']

        #  first remove() should not shrink the array, since with 16 elements
        #  we have not passed the N/4 threshold.
        da.remove('a')

        self.assertEqual(da._capacity, 64)

        #  second remove() should trigger halving the array capacity:
        da.remove('q')

        self.assertEqual(da._capacity, 32)

    def test_pop_raises_Empty_exception_if_array_is_empty(self):
        da = DynamicArray()

        self.assertRaises(Empty, da.pop)

    def test_pop_removes_and_returns_last_element_of_array(self):
        da = DynamicArray()
        da._n = 3
        da._capacity = 3
        da._A = da._make_array(da._capacity)
        da._A[0:3] = ['foo', 'bar', 'baz']

        result = da.pop()

        self.assertEqual(result, 'baz')
        self.assertEqual(da._A[0:2], ['foo', 'bar'])
        self.assertEqual(da._n, 2)

    def test_pop_halves_array_capacity_if_less_than_quarter_of_capacity_used(self):
        da = DynamicArray()
        da._capacity = 64
        da._n = 17
        da._A = da._make_array(da._capacity)
        da._A[0:17] = [None] * 17

        #  first pop() should not shrink the array, since with 16 elements
        #  we have not passed the N/4 threshold.
        da.pop()

        self.assertEqual(da._capacity, 64)

        #  second pop() should trigger halving the array capacity:
        da.pop()

        self.assertEqual(da._capacity, 32)
