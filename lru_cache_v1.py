
class LRUCache:
    """
    Approach - Using Ordered dict
    """
    def __init__(self,capacity) -> None:
        self.capacity = capacity
        self._cache = {}

    def put(self,key,val):
        """
        O(1)
        """
        if key in self._cache:
            self._cache.pop(key)
        self._cache[key] = val
        if len(self._cache) > self.capacity:
            self._cache.pop(next(iter(self._cache)))

    def get(self,key):
        """
        O(1)
        """
        if key in self._cache:
            self._cache[key] = self._cache.pop(key)
            return self._cache[key]
        return None


if __name__=='__main__':
    lru = LRUCache(2)
    lru.put(1,10)
    print(lru._cache)
    lru.put(2,20)
    print(lru._cache)
    lru.put(1,11)
    print(lru._cache)
    lru.put(3,30)
    print(lru._cache)