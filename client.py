"""Counting Bloom Filter Supporting Safe Deletion.
100% Python Standard Library.
"""

import hashlib

class CountingBloomFilter:
    """Counting Bloom Filter supporting insertion, deletion, and query without false negatives."""
    def __init__(self, size=64, num_hashes=3):
        self.size = size
        self.k = num_hashes
        self.counters = [0] * size

    def _hashes(self, item):
        h1 = int(hashlib.md5(str(item).encode("utf-8")).hexdigest()[:8], 16)
        h2 = int(hashlib.sha256(str(item).encode("utf-8")).hexdigest()[:8], 16)
        return [(h1 + i * h2) % self.size for i in range(self.k)]

    def add(self, item):
        for idx in self._hashes(item):
            self.counters[idx] += 1

    def remove(self, item):
        indices = self._hashes(item)
        if any(self.counters[idx] <= 0 for idx in indices):
            return False
        for idx in indices:
            self.counters[idx] -= 1
        return True

    def contains(self, item):
        return all(self.counters[idx] > 0 for idx in self._hashes(item))
