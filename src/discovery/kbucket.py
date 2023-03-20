from discovery.util import bytes_to_bit_string
from itertools import chain
from collections import OrderedDict
from discovery.util import shared_prefix
import time

class KBucket:
    def __init__(self, rangeLower, rangeUpper, ksize, replacementNodeFactor=5):
        self.range = (rangeLower, rangeUpper)
        self.nodes= OrderedDict()
        self.replacementNodes = OrderedDict()
        self.touch_last_updated()
        self.ksize = ksize
        self.maxReplacementNodes = self.ksize * replacementNodeFactor

    def get_nodes(self):
        return list(self.nodes.values())

    def head(self):
        return list(self.nodes.values())[0]

    def touch_last_updated(self):
        self.last_updated = time.monotonic()

    def has_in_range(self, node):
        result=self.range[0] <= node.long_id <= self.range[1]
        print(f"KBucket::has_in_range: node: {node.id}, result: {result}")
        return result

    def is_new_node(self, node):
        return node.id not in self.nodes
    
    def add_node(self, node):
        if node.id in self.nodes:
            print(f"KBucket::add_node already in self.nodes: node: {node.id}")
            del self.nodes[node.id]
            self.nodes[node.id] = node
        elif len(self) < self.ksize:
            print(f"KBucket::add_node: enough room: node: {node.id}, len(self): {len(self)} < self.ksize: {self.ksize}")
            self.nodes[node.id] = node
        else:
            print(f"KBucket::add_node: full: node:{node.id}")
            if node.id in self.replacementNodes:
                print(f"KBucket:add_node: already in replaceNodes: node:{node.id}")
                del self.replacementNodes[node.id]
            self.replacementNodes[node.id] = node
            while len(self.replacementNodes) > self.maxReplacementNodes:
                self.replacementNodes.popitem(last=False)
            return False
        return True

    def split(self):
        midpoint = (self.range[0] + self.range[1]) // 2
        one = KBucket(self.range[0], midpoint, self.ksize)
        two = KBucket(midpoint + 1, self.range[1], self.ksize)
        nodes = chain(self.nodes.values(), self.replacementNodes.values())
        for node in nodes:
            bucket = one if node.long_id <= midpoint else two
            bucket.add_node(node)
         
        return (one, two)

    def depth(self):
        vals = self.nodes.values()
        print(f"KBucket::depth: vals:{vals}")
        sprefix = shared_prefix([bytes_to_bit_string(n.id) for n in vals])
        print(f"KBucket::depth: {len(sprefix)}")
        return len(sprefix)
        

    def __len__(self):
        return len(self.nodes)

    def remove_node(self, node):
        if node.id in self.replacementNodes:
            del self.replacementNodes[node.id]
        
        if node.id in self.nodes:
            del self.nodes[node.id]
            
            if self.replacementNodes:
                newnode_id, newnode = self.replacementNodes.popitem()
                self.nodes[newnode_id] = newnode

