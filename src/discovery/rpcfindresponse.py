from discovery.node import Node

class RPCFindResponse:
    def __init__(self, response):
        self.response = response

    def happened(self):
        return self.response[0]

    def get_node_list(self):
        nodelist = self.response[1] or []
        return [Node(*nodeple) for nodeple in nodelist]
