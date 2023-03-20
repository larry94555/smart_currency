import asyncio
import heapq
from discovery.kbucket import KBucket
import operator
from discovery.tabletraverser import TableTraverser

class RoutingTable:
    def __init__(self, protocol, ksize, node):
        self.node = node
        self.protocol = protocol
        self.ksize = ksize
        self.flush()

    def add_contact(self, node):
        print(f"RoutingTable::add_contact: node.id: {node.id}")
        index = self.get_bucket_for(node)
        bucket = self.buckets[index]
        
        if bucket.add_node(node):
            print(f"RoutingTable::add_contact: enough space: bucket_add_node: node: {node.id}...")
            return

        if bucket.has_in_range(self.node) or bucket.depth() % 5 != 0:
            print(f"RoutingTable::add_contact has_in_range or depth() %5 != 0")
            self.split_bucket(index)
            self.add_contact(node)
        else:
            print(f"RoutingTable::add_contact: Calling ping...")
            asyncio.ensure_future(self.protocol.call_ping(bucket.head()))

    def find_neighbors(self, node, k=None, exclude=None):
        k = k or self.ksize
        nodes = []
        for neighbor in TableTraverser(self, node):
            notexcluded = exclude is None or not neighbor.same_home_as(exclude)
            if neighbor.id != node.id and notexcluded:
                heapq.heappush(nodes, (node.distance_to(neighbor), neighbor))
            if len(nodes) == k:
                break

        return list(map(operator.itemgetter(1), heapq.nsmallest(k, nodes)))

    def flush(self):
        self.buckets = [KBucket(0, 2 ** 260, self.ksize)]

    def get_bucket_for(self, node):
        #print(f"RoutingTable::get_bucket_for: node: {node.id}")
        for index, bucket in enumerate(self.buckets):
            #print(f"RoutingTable::get_bucket_for: index: {index}, node.id: {node.id}, range: {bucket.range[1]}")
            if node.long_id < bucket.range[1]:
                print(f"RoutingTable::get_bucket_for: returning index: {index}, node: {node.id}")
                return index
        print("RoutingTable::get_bucket_for: Returning None....")
        return None

    def is_new_node(self, node):
        index = self.get_bucket_for(node)
        isNew = self.buckets[index].is_new_node(node)
        print(f"RoutingTable::is_new_node: bucket index: {index}, node.id: {node.id}, isNew: {isNew}") 
        return isNew

    def split_bucket(self, index):
        one, two = self.buckets[index].split()
        self.buckets[index] = one
        self.buckets.insert(index+1, two)

    def remove_contact(self, node):
        index = self.get_bucket_for(node)
        self.buckets[index].remove_node(node)
