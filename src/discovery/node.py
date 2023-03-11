import discovery.util as util

class Node:
    """
    Main class that handles the following features:
    1.  Join
    2.  Broadcast
    3.  Count
    4.  Regenerate Key
    """
    def __init__(self, id=0, host="127.0.0.1", port=1024, nextAvailable=True):
        print("Node::init")
        self.host = host
        self.port = util.findNextPort(port) if nextAvailable else port
        # generate private/public key if needed

    def join(self, node=None):
        if node == None:
            print("Node::join None")
        else:
            print("Node::join existing...") 

    def regenerateKey(self):
        print("Node::regenerateKey")

    def broadcast(self, message):
        print("Node::broadcast")
        return "OK"

    def count(self, message=None):
        print("Node::count")
        return 0
