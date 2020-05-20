import unittest
from pythondsa.src.arrays import DynamicArray


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

    #  def test_insert_adds_at_index_shifts_items_...with_negative_index(self):
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
