import heapq
from operator import itemgetter

class NodeHeap:

    def __init__(self, node, maxsize):
        self.node = node
        self.heap = []
        self.contacted = set()
        self.maxsize = maxsize

    def push(self, nodes):
        if not isinstance(nodes, list):
            nodes = [nodes]
        
        for node in nodes:
            if node not in self:
                distance = self.node.distance_to(node)
                heapq.heappush(self.heap, (distance, node))

    def get_ids(self):
        return [n.id for n in self]

    def have_contacted_all(self):
        return len(self.get_uncontacted()) == 0

    def remove(self, peers):
        peers = set(peers)
        if not peers:
            return
        nheap = []
        for distance, node in self.heap:
            if node.id not in peers:
                heapq.heappush(nheap, (distance, node))
        self.heap = nheap

    def get_uncontacted(self):
        return [n for n in self if n.id not in self.contacted]

    def mark_contacted(self,node):
        self.contacted.add(node.id)

    def __len__(self):
        return min(len(self.heap), self.maxsize)

    def __contains__(self, node):
        for _, other in self.heap:
            if node.id == other.id:
                return True
        return False

    def __iter__(self):
        nodes = heapq.nsmallest(self.maxsize, self.heap)
        return iter(map(itemgetter(1), nodes))
