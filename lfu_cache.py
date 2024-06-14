class LFUCache:
    """
    What ?
        - It is a caching algorithm used in computer science to manage the contents of a cache
            - retains most frequently used items
            - discards least frequently accessed items when the cache reaches its capacity

    Why ?
        - reduces latency and bandwidth usage by prioritizing content that is accessed frequently by users


    Where ?
        - LFU caching is effective in scenarios where certain items are accessed much more frequently than others

        - It's often used in web servers, databases, operating systems, and 
        various other software systems to improve response times

    How ?
        - Each item in the cache is associated with a counter 
        that keeps track of how frequently the item is accessed.

        - Whenever an item in the cache is accessed, 
        its associated counter is incremented to reflect the increased access frequency.

        - (Eviction Policy) When the cache is full and needs to evict an item to make room for a new one, 
        the LFU algorithm identifies the item with the lowest access frequency count. 

        - During eviction, a tie may occue (i.e., multiple items have the same lowest access frequency count), 
        As a tiebreaker, one common approach is to use the Least Recently Used (LRU) policy, 
        removing the least recently accessed item among those with the lowest access frequency.

    """
    def __init__(self,capacity) -> None:
        self._capacity = capacity
        self._frequency = {}
        self._cache = {}
    
    def __str__(self) -> str:
        return str(self._cache)

    def get(self,key):
        """
        O(1)
        """
        # Increment frequency if key already present
        if key in self._cache:
            self._frequency[key] += 1
            return self._cache[key]
        return None
    
    def put(self,key,val):
        """
        O(n) - worst case during eviction when we find min freq
        """
        # Update key if already present
        if key in self._cache:
            self._frequency[key] += 1
            self._cache[key] = val
            return
        # Evict least frequently used item(s) if capacity exceeded
        if len(self._cache) >= self._capacity:
            min_freq = min(self._frequency.values())
            keys_to_remove = [k for k,v in self._frequency.items() if v == min_freq]
            for k in keys_to_remove:
                del self._cache[k]
                del self._frequency[k]
        # Insert new
        self._frequency[key] = 1
        self._cache[key] = val

if __name__=='__main__':
    lfu = LFUCache(2)
    lfu.put(1,10)
    print(lfu._cache,lfu._frequency)
    lfu.put(2,20)
    print(lfu._cache,lfu._frequency)
    lfu.put(1,11)
    print(lfu._cache,lfu._frequency)
    # lfu.put(1,12)
    # print(lfu._cache,lfu._frequency)
    lfu.put(2,21)
    print(lfu._cache,lfu._frequency)
    lfu.put(3,30)
    print(lfu._cache,lfu._frequency)