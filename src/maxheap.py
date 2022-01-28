"""Max heap algorithm

########################################################################
This implementation is completely based on the implementation of the 
standard `heapq` module
########################################################################

Max heap are arrays for which a[k] >= a[2*k+1] and a[k] >= a[2*k+2] for
all k, counting elements from 0.  For the sake of comparison,
non-existing elements are considered to be infinite.  The interesting
property of a max heap is that a[0] is always its biggest element.

Usage:

heap = []            # creates an empty heap
heappush(heap, item) # pushes a new item on the heap
item = heappop(heap) # pops the biggest item from the heap
item = heap[0]       # biggest item on the heap without popping it
heapify(array)       # transforms list into a heap, in-place, in linear time
item = heapreplace(heap, item) # pops and returns biggest item, and adds
                               # new item; the heap size is unchanged
item = heappushpop(heap, item) # adds new item, pops and returns biggest
                               # item
"""

__about__ = """
Max heap are arrays for which a[k] >= a[2*k+1] and a[k] >= a[2*k+2] for
all k, counting elements from 0.  For the sake of comparison,
non-existing elements are considered to be infinite.  The interesting
property of a max heap is that a[0] is always its biggest element.

                                 98

                 98                              97

          94             93              95               88

     87       93     73       90     68      91       87       75
"""

__all__ = ['heapush,', 'heappop', 'heapify', 'heapreplace', 'merge'
           'nlargest', 'nsmallest', 'heappushpop']

from typing import Any, Callable, Generator, Iterable, TypeVar

_T = TypeVar('_T')


def heappush(heap: list[_T], item: _T) -> None:
    """
    Push item onto heap, maintaining the heap invariant.

    :param heap:
    :param item:
    :return:
    """
    heap.append(item)
    _siftup(heap, len(heap) - 1)

def heappop(heap: list[_T]) -> _T:
    """
    Pop the biggest item off the heap, maintaining the heap invariant

    :param heap:
    :return lastelt:
    """
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    if heap:
        return_item = heap[0]
        heap[0] = lastelt
        _siftdown(heap, 0)
        return return_item
    return lastelt


def heapreplace(heap: list[_T], item: _T) -> _T:
    """
    Pop and return the current biggest value, and add the new item.

    This is more efficient than heappop() followed by heappush(), and can be
    more appropriate when using a fixed-size heap.  Note that the value
    returned may be larger than item!

    :param heap:
    :param item:
    :return return_item:
    """
    return_item = heap[0]
    heap[0] = item
    _siftdown(heap, 0)
    return return_item


def heappushpop(heap: list[Any], item: _T) -> _T:
    """
    Fast version of a heappush followed by a heappop.

    :param heap:
    :param item:
    :return item:
    """
    if heap and heap[0] > item:
        item, heap[0] = heap[0], item
        _siftdown(heap, 0)
    return item

def heapify(array: list[Any]) -> None:
    """
    Transform list into a heap, in-place, in O(len(x)) time.
    Transform bottom-up.  The largest index there's any point to
    looking at is the largest with a child index in-range, so must
    have 2*i + 1 < n, or i < (n-1)/2.

    :param array:
    :return:
    """
    n = len(array)
    for i in reversed(range(n//2)):
        _siftdown(array, i)


def _siftup(heap: list[_T], pos: int) -> None:
    """
    Follow the path to the root, moving parents down until finding a
    place cur_item fits.

    :param heap:
    :param pos:
    :return:
    """
    cur_item = heap[pos]
    while pos > 0:
        parent_pos = (pos - 1) >> 1
        if cur_item > heap[parent_pos]:
            heap[pos] = heap[parent_pos]
            pos = parent_pos
            continue
        break
    heap[pos] = cur_item


def _siftdown(heap: list[_T], pos: int) -> None:
    """
    Go down the tree until cur_item has no more children.

    :param heap:
    :param pos:
    "return:
    """
    cur_item = heap[pos]
    child_pos = (2 * pos) + 1
    while child_pos < len(heap):
        right_pos = child_pos + 1
        if right_pos < len(heap) and heap[child_pos] < heap[right_pos]:
            child_pos = right_pos
        if cur_item < heap[child_pos]:
            heap[pos] = heap[child_pos]
            pos = child_pos
            child_pos = (2 * pos) + 1
            continue
        break
    heap[pos] = cur_item
    


def merge(*iterables: list[Iterable], key: Callable = None,
           reverse: bool = False) -> Generator:
    '''
    Merge multiple sorted inputs into a single sorted output.

    Similar to sorted(itertools.chain(*iterables)) but returns a generator,
    does not pull the data into memory all at once, and assumes that each of
    the input streams is already sorted (largest to smallest).

    If *key* is not None, applies a key function to each element to determine
    its sort order.

    >>> 
    '''
    h = []
    if key is None:
        for order, it in enumerate(map(iter,iterables)):
            try:
                next = it.__next__
                h.append([next(), order, next])
            except StopIteration:
                pass
            heapify(h)
        while len(h) > 1:
            try:
                while True:
                    value, order, next = s = h[0]
                    yield value
                    s[0] = next()           # raise StopIteration when exhausted
                    heapreplace(h, s)       # restore heap condition
            except StopIteration:
                heappop(h)                  # remove empty iterator
        if h:
            # fast case when only a single itarator remains
            try:
                value, *other, next = h[0]
                yield value
                while True:
                    yield next()
            except StopIteration:
                pass
        return
    for order, it in enumerate(map(iter, iterables)):
        try:
            next = it.__next__
            value = next()
            h.append([key(value), order, value, next])
        except StopIteration:
            pass
    heapify(h)
    while len(h) > 1:
        try:
            while True:
                key_value, order, value, next = s = h[0]
                yield value
                value = next()
                s[0] = key(value)
                s[2] = value
                heapreplace(h, s)
        except StopIteration:
            heappop(h)
    if h:
        try:
            *others, value, next = h[0]
            yield value
            while True:
                yield next()
        except StopIteration:
            pass