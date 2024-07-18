import time

class LRUCache:
    """
    What:
        - It is a caching algorithm used to manage the contents of a cache
            - retains most recently used items
            - discards the least recently used items when the cache reaches its capacity

    Why:
        - to improve cache performance by prioritizing items that have been accessed recently, 
        under the assumption that they are more likely to be accessed again in the near future. 
        
        - By evicting the least recently used items, the cache maximizes the chances of retaining frequently accessed data, 
        thus reducing cache misses and improving overall system performance        
    
    Where:
        - LRU caching is commonly used in scenarios where there is temporal locality in data access patterns, 
        meaning that recently accessed data is more likely to be accessed again soon. 

        - It's often used in web servers, databases, operating systems, and 
        various other software systems to improve response times and optimize resource utilization.
    
    How:
        - Each item in the LRU cache is associated with a timestamp 
        or some form of metadata indicating when it was last accessed

        - Whenever an item in the cache is accessed, its associated timestamp is updated to reflect the current time, 
        indicating that it is now the most recently used item
        
        - (Eviction Policy) - When the cache is full and needs to evict an item to make room for a new one, 
        the LRU algorithm identifies the item that was least recently accessed 
        (i.e., the item with the oldest timestamp).
    """
    def __init__(self,capacity) -> None:
        self._capacity = capacity
        self._timestamp = {}
        self._cache = {}
    
    def __str__(self) -> str:
        return str(self._cache)
    
    def get(self,key):
        """
        O(1)
        """
        if key not in self._cache:
            return None
        else:
            self._timestamp[key] = time.time()
            return self._cache[key]
    
    def put(self,key,val):
        """
        O(n) - Worst case during eviction when we find oldest keys
        """
        if key in self._cache:
            self._timestamp[key] = time.time()
            self._cache[key] = val
            return
        if len(self._cache) >= self._capacity:
            oldest_timestamp = min(self._timestamp.values())
            keys_to_remove = [k for k,v in self._timestamp.items() if v == oldest_timestamp]
            for k in keys_to_remove:
                del self._cache[k]
                del self._timestamp[k]
        self._timestamp[key] = time.time()
        self._cache[key] = val

if __name__=='__main__':
    lru = LRUCache(2)
    lru.put(1,10)
    print(lru._timestamp, lru._cache)
    lru.put(2,20)
    print(lru._timestamp, lru._cache)
    lru.put(1,11)
    print(lru._timestamp, lru._cache)
    lru.put(3,30)
    print(lru._timestamp, lru._cache)