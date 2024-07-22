class Node:
    def __init__(self,key=None,val=None,freq=1,next=None,prev=None) -> None:
        self.key = key
        self.val = val
        self.freq = freq
        self.next = next
        self.prev = prev
    
    def __str__(self) -> str:
        return f'Node({self.key},{self.val},{self.freq})'
    
    def __repr__(self) -> str:
        return str(self)
    
class DLL:
    def __init__(self) -> None:
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def __str__(self) -> str:
        return '<->'.join([str(node) for node in self])
    
    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        curr = self.head.next
        while curr.next:
            yield curr
            curr = curr.next

    def insert(self,node):
        """
        Inserts at the tail
        O(1)
        """
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
        self.size += 1
    
    def delete(self,node):
        """
        Deletes the node from its position
        O(1)
        """
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

class LFUCache:
    """
    Initial:
        cache:  {}
        freq_map: {}
        min_freq: 1

    Insert Node(Apple,40): Not Exists
        cache:      {'Apple': Node(Apple,40,1)}
        freq_map:   {1: Node(Apple,40,1)} 
        min_freq:   1   

    Insert Node(Banana,20): Not Exists
        cache:      {'Apple': Node(Apple,40,1), 'Banana': Node(Banana,20,1)}
        freq_map:   {1: Node(Apple,40,1)<->Node(Banana,20,1)}
        min_freq:   1 
    
    Update Node(Apple,110): Exists
        cache:      {'Apple': Node(Apple,110,2), 'Banana': Node(Banana,20,1)}
        freq_map:   {1: Node(Banana,20,1), 2: Node(Apple,110,2)}
        min_freq:   1 
    
    Insert Node(Orange,30): Not Exists and capcity exceeded
        cache:      {'Apple': Node(Apple,110,2), 'Orange': Node(Orange,30,1)}
        freq_map:   {1: Node(Orange,30,1), 2: Node(Apple,110,2)}
        min_freq:   1

    Insert Node(Mango,40): Not Exists and capcity exceeded
        cache:      {'Apple': Node(Apple,110,2), 'Mango': Node(Mango,40,1)}
        freq_map:   {1: Node(Mango,40,1), 2: Node(Apple,110,2)}
        min_freq:   1

    Update Node(Mango,41): Exists
        cache:      {'Apple': Node(Apple,110,2), 'Mango': Node(Mango,41,2)}
        freq_map:   {1: , 2: Node(Apple,110,2)<->Node(Mango,41,2)}
        min_freq:   2

    Insert Node(Orange,30): Not Exists and capcity exceeded
        cache:      {'Mango': Node(Mango,41,2), 'Orange': Node(Orange,30,1)}
        freq_map:   {1: Node(Orange,30,1), 2: Node(Mango,41,2)}
        min_freq:   1
    """
    def __init__(self,capacity) -> None:
        self.capacity = capacity
        self.cache = {}                     # Maps keys to individual node objects
        self.freq_map = {}                  # Maps freq to DLL of node objects having that frequency
        self.min_freq = 1

    def _update(self,node):
        """
        Updates the node by 
            deleting it from previous freq list and
            adding to the updated freq list
        """
        self._delete_from_freq_map(node)    # delete node from prev freq list    
        if self.freq_map[self.min_freq].size == 0:
            self.min_freq += 1              # increment min freq if the DLL of that freq has no nodes
        node.freq += 1                      # increment node freq
        self._add_to_freq_map(node)         # add node to updated freq list

    def _delete_from_freq_map(self,node):
        """
        Deletes the node from the corresponding freq list
        """
        self.freq_map[node.freq].delete(node)

    def _add_to_freq_map(self,node):
        """
        Adds the node to the corresponding freq list
        """
        self.freq_map[node.freq] = self.freq_map.get(node.freq,DLL())
        self.freq_map[node.freq].insert(node)

    def put(self,key,val):
        """
        if key is present in cache
            update its value
            delete it from previous freq list and add it to updated freq list
            also update min freq if the previous freq list gets empty
        else
            if cache is at capacity
                find the list having min freq (LFU Nodes)
                if multiple nodes having min freq, delete the head (LRU among the LFU nodes)
            Create new node and add to cache and freq map
            Reset min freq to 1
        """
        if key in self.cache:
            node = self.cache[key]
            node.val = val
            self._update(node)
        else:
            if len(self.cache) == self.capacity:
                lfu_dll = self.freq_map[self.min_freq]
                lfu_node = lfu_dll.head.next
                lfu_dll.delete(lfu_node)
                del self.cache[lfu_node.key]
            node = Node(key,val)
            self.cache[key] = node
            self.min_freq = 1
            self._add_to_freq_map(node)

    def get(self,key):
        """
        if key exists in cache
            delete the node from previous freq list and add it to updated freq list
            also update min freq if the previous freq list gets empty
            return node val
        else return -1
        """
        if key in self.cache:
            node = self.cache[key]
            self._update(node)
            return node.val
        return -1

if __name__=='__main__':
    lfu = LFUCache(2)
    lfu.put("Apple",40)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put("Banana",20)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put("Apple",110)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put("Orange",30)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put("Mango",40)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put("Mango",41)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put("Orange",30)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
