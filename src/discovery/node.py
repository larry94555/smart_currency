
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

    def same_home_as(self, node):
        return self.sender[0] == node.sender[0] and self.sender[1] == node.sender[1]

    def distance_to(self, node):
        return self.long_id ^ node.long_id

    def __iter__(self):
        return iter([self.id, self.sender])

    def __repr__(self):
        return repr([self.long_id, self.sender])

    def __str__(self):
        return f"{self.sender[0]}:{str(self.sender[1])}"


    
