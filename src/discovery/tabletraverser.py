
class TableTraverser:
    def __init__(self, router, startNode):
        index = router.get_bucket_for(startNode)
        router.buckets[index].touch_last_updated()
        self.current_nodes = router.buckets[index].get_nodes()
        self.left_buckets = router.buckets[:index]
        self.right_buckets = router.buckets[(index+1):]
        self.left = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_nodes:
            return self.current_nodes.pop()

        if self.left and self.left_buckets:
            self.current_nodes = self.left_buckets.pop().get_nodes()
            self.left = False
            return next(self)

        if self.right_buckets:
            self.current_nodes = self.right_buckets.pop(0).get_nodes()
            self.left = True
            return next(self)

        raise StopIteration 
