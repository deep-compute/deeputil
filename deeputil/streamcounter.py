from collections import Counter

class StreamCounter(object):
    '''
    '''
    #TODO Doctests and examples
    DEFAULT_CHUNK_SIZE = 1000000
    DEFAULT_MAX_COUNTS = 1000000

    def __init__(self, chunk_size=DEFAULT_CHUNK_SIZE,
        max_counts=DEFAULT_MAX_COUNTS):

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
        self.counts[item] += count
        self.counts_total += count

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
        chunk_id = min(self.chunked_counts.keys())
        chunk = self.chunked_counts.pop(chunk_id)

        self.n_counts -= len(chunk)
        for k, v in list(chunk.items()):
            self.counts[k] -= v
            self.counts_total -= v

    def get(self, item, default=0, normalized=False):
        c = self.counts.get(item, default)
        if not normalized:
            return c

        return c / float(self.counts_total)

    def __getitem__(self, k):
        return self.get(k)
