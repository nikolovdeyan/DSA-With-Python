import unittest
from pythondsa.src.maps import UnsortedTableMap, ChainHashMap
from pythondsa.src.maps import TreeMap


class TestUnsortedTableMap(unittest.TestCase):

    def test_getitem_raises_KeyError_if_key_not_in_map(self):
        utm = UnsortedTableMap()
        utm._table = [utm._Item('foo', 1), utm._Item('bar', 2)]

        self.assertRaises(KeyError, utm.__getitem__, 'baz')

    def test_getitem_returns_item_value_for_matching_key_in_map(self):
        utm = UnsortedTableMap()
        expected_key, expected_value = 'baz', 3
        utm._table = [utm._Item('foo', 1), utm._Item(expected_key, expected_value)]

        result_value = utm[expected_key]

        self.assertEqual(result_value, expected_value)

    def test_setitem_assigns_value_to_key_overwriting_if_key_present(self):
        utm = UnsortedTableMap()
        expected_key, expected_value = 'foo', 1

        utm[expected_key] = expected_value

        self.assertEqual(utm._table[0]._key, expected_key)
        self.assertEqual(utm._table[0]._value, expected_value)

        expected_value = 'bar'

        utm[expected_key] = expected_value

        self.assertEqual(utm._table[0]._value, expected_value)

    def test_delitem_raises_KeyError_if_key_not_in_map(self):
        utm = UnsortedTableMap()
        unexpected_key = 'foo'

        self.assertRaises(KeyError, utm.__delitem__, unexpected_key)

    def test_delitem_removes_item_associated_with_key_in_map(self):
        utm = UnsortedTableMap()
        key_to_delete, value_to_delete = 'foo', 1
        utm._table = [utm._Item(key_to_delete, value_to_delete), utm._Item('bar', 2)]

        del(utm[key_to_delete])

        self.assertNotEqual(utm._table[0]._key, key_to_delete)
        self.assertNotEqual(utm._table[0]._value, value_to_delete)

    def test_len_returns_number_of_items_in_map(self):
        utm = UnsortedTableMap()
        utm._table = [
            utm._Item('foo', 1),
            utm._Item('bar', 2),
            utm._Item('baz', 3),
        ]
        expected_result = 3

        result = len(utm)

        self.assertEqual(result, expected_result)

    def test_iter_generates_iterations_of_maps_keys(self):
        utm = UnsortedTableMap()
        utm._table = [
            utm._Item('foo', 1),
            utm._Item('bar', 2),
            utm._Item('baz', 3),
        ]
        expected_result = ['foo', 'bar', 'baz']

        result = [k for k in utm]

        self.assertEqual(result, expected_result)


class TestChainHashMap(unittest.TestCase):

    def test_getitem_raises_KeyError_if_key_not_in_map(self):
        chm = ChainHashMap()

        self.assertRaises(KeyError, chm.__getitem__, 'spam')

    def test_getitem_returns_item_value_for_matching_key_in_map(self):
        chm = ChainHashMap()
        expected_key = 'spam'
        expected_value = 'eggs'
        bucket = UnsortedTableMap()
        expected_item = bucket._Item(expected_key, expected_value)
        bucket._table = [expected_item]
        chm._table[2] = bucket
        # override hash function to return index
        chm._hash_function = lambda x: 2
        chm._n = 1

        result = chm[expected_key]

        self.assertEqual(result, expected_value)


class TestTreeMap(unittest.TestCase):

    def test_getitem_raises_KeyError_if_key_not_in_map(self):
        tm = TreeMap()

        self.assertRaises(KeyError, tm.__getitem__, 'spam')
