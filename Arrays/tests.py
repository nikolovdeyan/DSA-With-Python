import unittest
from arrays import DynamicArray


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

    def test_getitem_returns_correct_element_at_index(self):
        expected_result = 'bar'
        elements = ['foo', expected_result, 'baz']
        da = DynamicArray()
        da._n = 3
        da._capacity = 4
        da._A = da._make_array(da._capacity)
        da._A[0:3] = elements

        result = da[1]

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
