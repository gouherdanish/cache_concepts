class Node:
    def __init__(self,key=None,val=None,next=None,prev=None) -> None:
        self.key = key
        self.val = val
        self.next = next
        self.prev = prev

    def __str__(self) -> str:
        return f'({self.key},{self.val})'
    
    def __repr__(self) -> str:
        return str(self)
    
class DLL:
    def __init__(self) -> None:
        self.length = 0
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert(self,node):
        "Inserts the given node just before the tail"
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node


    def delete(self,node):
        """
        Deletes the given node from its position. 
        No need to traverse from head to the node
        """
        node.next.prev = node.prev
        node.prev.next = node.next


class LRUCache:
    """
    Initial:
        cache:  {}
        dll:    Head -> Dummy <-> Dummy <- Tail

    Insert Node(1,10): Not Exists
        cache:  {1: Node(1,10)}
        dll:    Head -> Dummy <-> Node(1,10) <-> Dummy <- Tail

    Insert Node(2,20): Not Exists
        cache:  {1, Node(1,10), 2: Node(2,20)}
        dll:    Head -> Dummy <-> Node(1,10) <-> Node(2,20) <-> Dummy <- Tail
    
    Insert Node(1,11): Exists
        cache:  {1, Node(1,11), 2: Node(2,20)}
        dll:    Head -> Dummy <-> Node(2,20) <-> Node(1,11) <-> Dummy <- Tail
    
    Insert Node(3,30): Not Exists and capcity exceeded
        cache:  {1, Node(1,11), 3: Node(3,30)}
        dll:    Head -> Dummy <-> Node(1,11) <-> Node(3,30) <-> Dummy <- Tail
    """
    def __init__(self,capacity) -> None:
        self.capacity = capacity
        self.dll = DLL()
        self.cache = {}

    def get(self,key):
        if key in self.cache:
            node = self.cache[key]
            self.dll.delete(node)
            self.dll.insert(node)
            return node.val
        return -1

    def put(self,key,val):
        if key in self.cache:
            self.dll.delete(self.cache[key])
        node = Node(key,val)
        self.cache[key] = node
        self.dll.insert(node)
        if len(self.cache) > self.capacity:
            lru = self.dll.head.next
            self.dll.delete(lru)
            del self.cache[lru.key]
        
if __name__=='__main__':
    lru = LRUCache(2)
    lru.put(1,10)
    print(lru.cache)
    lru.put(2,20)
    print(lru.cache)
    lru.put(1,11)
    print(lru.cache)
    lru.put(3,30)
    print(lru.cache)