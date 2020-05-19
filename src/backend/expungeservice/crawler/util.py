# Adapted from https://www.kunxi.org/2014/05/lru-cache-in-python/

import collections


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache: collections.OrderedDict = collections.OrderedDict()

    def __getitem__(self, key):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return None

    def __setitem__(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value
