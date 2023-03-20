
class Node:
    """
    This is public information associated iwth a node.
    It includes:
    1.  Public Key
    2.  Host
    3.  Port
    """
    def __init__(self, id, sender):
        print(f"Node::init: id: {id}, sender:{sender}")
        self.id = id
        self.sender = sender
        self.port = sender[1]
        self.long_id = int(id, 16)


    
