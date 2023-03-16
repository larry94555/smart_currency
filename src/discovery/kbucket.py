from collections import OrderedDict
import time

class KBucket:
    def __init__(self, rangeLower, rangeUpper, ksize, replacementNodeFactor=5):
        self.range = (rangeLower, rangeUpper)
        self.neighbors= OrderedDict()
        self.replacementNodes = OrderedDict()
        self.touch_last_updated()
        self.ksize = ksize
        self.maxReplacementNodes = self.ksize * replacementNodeFactor

    def touch_last_updated(self):
        self.last_updated = time.monotonic()

    def is_new_neighbor(self, neighbor):
        return neighbor.id not in self.neighbors
    
    def add_neighbor(self, neighbor):
        if neighbor.id in self.neighbors:
            del self.neighbors[neighbor.id]
            self.neighbors[neighbor.id] = neighbor
        elif len(self) < self.ksize:
            self.neighbors[neighbor.id] = neighbor
        else:
            if neighbor.id in self.replacementNodes:
                del self.replacementNodes[neighbor.id]
            self.replacementNodes[neighbor.id] = neighbor
            while len(self.replacementNodes) > self.maReplacementNodes:
                self.replacementNodes=popitem(last=False)
            return False
        return True

    def __len__(self):
        return len(self.neighbors)
         
