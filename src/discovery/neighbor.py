
class Neighbor:
    """
    This is public information associated iwth a node.
    It includes:
    1.  Public Key
    2.  Host
    3.  Port
    """
    def __init__(self, id, sender):
        print(f"Neighbor::init: id: {id}, sender:{sender}")
        self.id = id
        self.sender = sender
        self.long_id = int(id, 16)

    
