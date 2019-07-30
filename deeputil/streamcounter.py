from collections import Counter


class StreamCounter(object):
    """
    A class whose responsibility is to get the count of items
    in data comming as a stream.
    """

    # TODO Doctests and examples
    # When we receive a stream of data, we fix the max size of chunk
    # Think of chunk as a container, which can only fit a fixed no. of items
    # This will help us to keep control over RAM usage
    DEFAULT_CHUNK_SIZE = 1000000
    # When we have a container, we also want to count the occurences of items
    # Max count will be maximum occurence of an item
    DEFAULT_MAX_COUNTS = 1000000

    def __init__(self, chunk_size=DEFAULT_CHUNK_SIZE, max_counts=DEFAULT_MAX_COUNTS):

        self.chunk_size = chunk_size
        self.max_counts = max_counts

        # Counts of items stored on a per chunk basis
        # Dict of dictionaries. Outer dict has chunk id as key
        # Inner dict has items as keys and values are counts within
        # that chunk
        self.chunked_counts = {}

        # Overall counts (keys are items and values are counts)
        self.counts = Counter()

        # Total chunks seen so far
        self.n_chunks = 0

        # Total items seen so far
        self.n_items_seen = 0

        # Total items seen in current chunk
        self.n_chunk_items_seen = 0

        # Total count entries
        self.n_counts = 0

        # Counts total
        self.counts_total = 0

    def add(self, item, count=1):
        """
        When we receive stream of data, we add them in the chunk
        which has limit on the no. of items that it will store.
        >>> s = StreamCounter(5,5)
        >>> data_stream = ['a','b','c','d']
        >>> for item in data_stream:
        ...     s.add(item)
        >>> s.chunk_size
        5
        >>> s.n_items_seen
        4
        >>> s.n_chunk_items_seen
        4
        >>> s.n_chunks
        0
        >>> from pprint import pprint
        >>> pprint(s.chunked_counts.get(s.n_chunks, {}))
        {'a': 1, 'b': 1, 'c': 1, 'd': 1}
        >>> s.counts_total
        4
        >>> data_stream = ['a','b','c','d','e','f','g','e']
        >>> for item in data_stream:
        ...     s.add(item)
        >>> s.chunk_size
        5
        >>> s.n_items_seen
        12
        >>> s.n_chunk_items_seen
        2
        >>> s.n_chunks
        2
        >>> s.chunked_counts.get(s.n_chunks, {})
        {'g': 1, 'e': 1}
        """
        self.n_items_seen += count
        self.n_chunk_items_seen += count

        # get current chunk
        chunk_id = self.n_chunks
        chunk = self.chunked_counts.get(chunk_id, {})
        self.chunked_counts[chunk_id] = chunk

        # update count in the current chunk counter dict
        if item in chunk:
            chunk[item] += count
        else:
            self.n_counts += 1
            chunk[item] = count

        # is the current chunk done?
        if self.n_chunk_items_seen >= self.chunk_size:
            self.n_chunks += 1
            self.n_chunk_items_seen = 0

        # In case we reached max capacity in count entries,
        # drop oldest chunks until we come back within limit
        while self.n_counts >= self.max_counts:
            self._drop_oldest_chunk()

    def _drop_oldest_chunk(self):
        """
        To handle the case when the items comming in the chunk
        is more than the maximum capacity of the chunk. Our intent
        behind is to remove the oldest chunk. So that the items come
        flowing in.
        >>> s = StreamCounter(5,5)
        >>> data_stream = ['a','b','c','d']
        >>> for item in data_stream:
        ...     s.add(item)
        >>> min(s.chunked_counts.keys())
        0
        >>> s.chunked_counts
        {0: {'a': 1, 'b': 1, 'c': 1, 'd': 1}}
        >>> data_stream = ['a','b','c','d','a','e','f']
        >>> for item in data_stream:
        ...     s.add(item)
        >>> min(s.chunked_counts.keys())
        2
        >>> s.chunked_counts
        {2: {'f': 1}}
        """
        chunk_id = min(self.chunked_counts.keys())
        chunk = self.chunked_counts.pop(chunk_id)

        self.n_counts -= len(chunk)
        for k, v in list(chunk.items()):
            self.counts[k] -= v
            self.counts_total -= v

    def get(self, item, default=0, normalized=False):
        """
        When we have the stream of data pushed in the chunk
        we can retrive count of an item using this method.
        >>> stream_counter_obj = StreamCounter(5,5)
        >>> data_stream = ['a','b','c']
        >>> for item in data_stream:
        ...     stream_counter_obj.add(item)
        >>> stream_counter_obj.get('a')
        1
        >>> stream_counter_obj.get('b')
        1
        >>> stream_counter_obj.get('c')
        1
        >>> stream_counter_obj.get('d')
        0
        >>> data_stream.extend(['d','e','f'])
        >>> for item in data_stream:
        ...     stream_counter_obj.add(item)
        >>> stream_counter_obj.get('a')
        0
        >>> stream_counter_obj.get('b')
        0
        >>> stream_counter_obj.get('c')
        1
        >>> stream_counter_obj.get('d')
        1
        >>> stream_counter_obj.get('e')
        1
        >>> stream_counter_obj.get('f')
        1
        """
        c = self.counts.get(item, default)
        if not normalized:
            return c

        return c / float(self.counts_total)

    def __getitem__(self, k):
        return self.get(k)
