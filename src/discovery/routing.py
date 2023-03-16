from discovery.kbucket import KBucket

class RoutingTable:
    def __init__(self, protocol, ksize, neighbor):
        self.neighbor = neighbor
        self.protocol = protocol
        self.ksize = ksize
        self.flush()

    def add_contact(self, neighbor):
        index = self.get_bucket_for(neighbor)
        bucket = self.buckets[index]
        
        if bucket.add_neighbor(neighbor):
            return

        if bucket.has_in_range(self.neighbor) or bucket.depth() % 5 != 0:
             self.split_bucket(index)
             self.add_contact(neighbor)
        else:
             asyncio.ensure_future(self.protocol.call_ping(bucket.head()))

    def flush(self):
        self.buckets = [KBucket(0, 2 ** 1024, self.ksize)]

    def get_bucket_for(self, neighbor):
        for index, bucket in enumerate(self.buckets):
            print(f"index: {index}, neighbor.long_id: {neighbor.long_id}, range: {bucket.range[1]}")
            if neighbor.long_id < bucket.range[1]:
                return index
        print("Returning None....")
        return None

    def is_new_neighbor(self, neighbor):
        index = self.get_bucket_for(neighbor)
        return self.buckets[index].is_new_neighbor(neighbor)
