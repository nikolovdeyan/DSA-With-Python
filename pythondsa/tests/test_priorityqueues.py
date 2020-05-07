import unittest
from unittest import mock
from pythondsa.src.doubly_linked import PositionalList
from pythondsa.src.priority_queues import UnsortedPriorityQueue


class TestUnsortedPriorityQueue(unittest.TestCase):

    #  Test PriorityQueueBase ABC's concrete methods:
    def test_is_empty_returns_correct_boolean_values(self):
        #  With an empty PositionalList
        with mock.patch.object(PositionalList, '__len__', return_value=0) as poslist:
            pq = UnsortedPriorityQueue()
            self.assertTrue(pq.is_empty())

        #  With a non-empty PositionalList
        with mock.patch.object(PositionalList, '__len__', return_value=1) as poslist:
            pq = UnsortedPriorityQueue()
            self.assertFalse(pq.is_empty())

    #  Test UnsortedPriorityQueue ABC's concrete methods:
    def test_len_returns_the_number_of_items_in_priority_queue(self):
        #  With an empty PositionalList
        with mock.patch.object(PositionalList, '__len__', return_value=0) as poslist:
            pq = UnsortedPriorityQueue()
            expected_result = 0

            result = len(pq)

            self.assertEqual(result, expected_result)

        #  With a non-empty PositionalList
        with mock.patch.object(PositionalList, '__len__', return_value=5) as poslist:
            pq = UnsortedPriorityQueue()
            expected_result = 5

            result = len(pq)

            self.assertEqual(result, expected_result)

    @mock.patch('pythondsa.src.priority_queues.PositionalList')
    def test_add_appends_item_with_key_value_pair_to_priority_queue_data(self, pl_mock):
        pq = UnsortedPriorityQueue()
        pq._data = pl_mock
        key, value = 'foo', 'bar'
        expected_item = pq._Item(key, value)

        pq.add(key, value)
        result_item = pl_mock.add_last.call_args.args[0]

        self.assertEqual(expected_item, result_item)
