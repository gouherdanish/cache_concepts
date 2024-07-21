class Node:
    def __init__(self,key=None,val=None,freq=1,next=None,prev=None) -> None:
        self.key = key
        self.val = val
        self.freq = freq
        self.next = next
        self.prev = prev
    
    def __str__(self) -> str:
        return f'{self.key}:{self.val}({self.freq})'
    
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
    def __init__(self,capacity) -> None:
        self.capacity = capacity
        self.cache = {}                     # Maps keys to individual node objects
        self.freq_map = {}                  # Maps freq to DLL of node objects having that frequency
        self.min_freq = 1

    def _update(self,node):
        # freq = node.freq
        self._delete_from_freq_map(node)    # delete node from prev freq list    
        if self.freq_map[self.min_freq].size == 0:
            self.min_freq += 1              # increment min freq if the DLL of that freq has no nodes
        node.freq += 1                      # increment node freq
        self._add_to_freq_map(node)         # add node to new freq list

    def _delete_from_freq_map(self,node):
        self.freq_map[node.freq].delete(node)

    def _add_to_freq_map(self,node):
        self.freq_map[node.freq] = self.freq_map.get(node.freq,DLL())
        self.freq_map[node.freq].insert(node)

    def put(self,key,val):
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
        if key in self.cache:
            node = self.cache[key]
            self._update(node)
            return node.val

if __name__=='__main__':
    lfu = LFUCache(2)
    lfu.put(1,10)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put(2,20)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put(1,11)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put(3,30)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put(4,40)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put(4,41)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
    lfu.put(3,30)
    print(lfu.cache,lfu.freq_map,lfu.min_freq)
