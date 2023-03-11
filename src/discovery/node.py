class Node:
    def __init__(self, host, port, nextAvailable=True):
        print("Node::init")

    def join(self, node=None):
        if node == None:
            print("Node::join None")
        else:
            print("Node::join existing...") 
