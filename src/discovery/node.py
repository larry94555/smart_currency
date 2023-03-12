import asyncio
from discovery.protocol import Protocol
import discovery.util as util

class Node:
    """
    Main class that handles the following features:
    1.  Join
    2.  Broadcast
    3.  Count
    4.  Regenerate Key
    """
    def __init__(self, id=0, host="127.0.0.1", port=1024, path="./test", nextAvailable=True):
        print("Node::init")
        self.host = host
        self.port = util.findNextPort(port) if nextAvailable else port
        self.path = f"{path}/instance{id}"
        self.get_public_and_private_keys()
        print(f"privateKey: {self._privateKey}, publicKey: {self._publicKey}")
        self.protocol_class = Protocol(self)

    def get_public_and_private_keys(self):
        self._privateKey, self._publicKey = util.get_keys(self.path)
        if self._privateKey is None or self._publicKey is None:
            self._privateKey, self._publicKey = util.create_keys(self.path)

    def create_protocol(self):
        return self.protocol_class

    def join(self, node=None):
        if node is not None:
            print("Node::join existing...") 

        # listen
        print(f"Node::listen: host: {self.host}, port: {self.port}")
        loop = asyncio.get_event_loop()
        listen = loop.create_datagram_endpoint(self.create_protocol,
                                               local_addr=(self.host, self.port))
        transport, protocol = loop.run_until_complete(listen)
        self.protocol_class.save_protocol_and_transport(protocol=protocol, transport=transport)
            
        
    def regenerateKey(self):
        print("Node::regenerateKey")

    def broadcast(self, message):
        print("Node::broadcast")
        return "OK"

    def count(self, message=None):
        print("Node::count")
        return 0
