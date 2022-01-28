from unittest import TestCase

from src.maxheap import heapify
from src.maxheap import merge
from src.maxheap import heappop
from src.maxheap import heapreplace
from src.maxheap import heappushpop
from src.maxheap import heappush


class TestMaxHeap(TestCase):
    def setUp(self):
        pass

    def test_max_heap_ivariant(self):
        test_array = [4, 6, 2, 1, 7, 9, 2, 6, 2, 1]
        heapify(test_array)
        for i in range(len(test_array)):
            cur_value = test_array[i]
            left_index = (2 * i) + 1
            right_index = left_index + 1
            if left_index < len(test_array):
                self.assertGreaterEqual(cur_value, test_array[left_index])
            if right_index < len(test_array):
                self.assertGreaterEqual(cur_value, test_array[right_index])

    def test_max_heap_invariant_with_negatives(self):
        test_array = [-7, 10, 12, -33, -4, 2, 5, 3, -99]
        heapify(test_array)
        for i in range(len(test_array)):
            cur_value = test_array[i]
            left_index = (2 * i) + 1
            right_index = left_index + 1
            if left_index < len(test_array):
                self.assertGreaterEqual(cur_value, test_array[left_index])
            if right_index < len(test_array):
                self.assertGreaterEqual(cur_value, test_array[right_index])

    def test_max_heap_invariant_with_real(self):
        test_array = [5.5, 3, 7.4, 7.7, 1, 3.33, 10.15]
        heapify(test_array)
        for i in range(len(test_array)):
            cur_value = test_array[i]
            left_index = (2 * i) + 1
            right_index = left_index + 1
            if left_index < len(test_array):
                self.assertGreaterEqual(cur_value, test_array[left_index])
            if right_index < len(test_array):
                self.assertGreaterEqual(cur_value, test_array[right_index])

    def test_max_heap_invariant_with_empty_array(self):
        test_array = []
        heapify(test_array)
        self.assertEqual(test_array, [])

    def test_pop_from_empty_heap(self):
        with self.assertRaises(IndexError):
            heappop([])

    def test_replace_with_empty_heap(self):
        with self.assertRaises(IndexError):
            heapreplace([], 1)

    def test_pushpop_with_empty_heap(self):
        self.assertEqual(heappushpop([], 4), 4)

    def test_push(self):
        test_heap = [32, 6, 13, 4, 5, 9, 1, 3]
        heappush(test_heap, 100)
        self.assertEqual(test_heap[0], 100)

    def test_merge_without_key(self):
        l1 = [5, 6, 2, 1, 3, 2]
        l2 = [7, 4 ,9 , 3, 1]
        l3 = (10,)
        l1 = sorted(l1, reverse=True)
        l2 = sorted(l2, reverse=True)
        l3 = sorted(l3, reverse=True)
        result = list(merge(l1, l2, l3))
        self.assertEqual(result, [10, 9, 7, 6, 5, 4, 3, 3, 2, 2, 1, 1])

    def test_merge_with_key(self):
        l1 = ['dog', 'horse']
        l2 = ['cat', 'fish', 'kangaroo']
        l1 = sorted(l1, key=len, reverse=True)
        l2 = sorted(l2, key=len, reverse=True)
        result = list(merge(l1, l2, key=len))
        self.assertEqual(result, ['kangaroo', 'horse', 'fish', 'cat', 'dog'])

    def test_merge_with_empty_collections(self):
        l1 = []
        l2 = set()
        l3 = tuple()
        result = list(merge(l1, l2, l3))
        self.assertEqual(result, [])