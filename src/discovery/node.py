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
        print(f"Node::init: port: {port}")
        self.host = host
        self.port = port
        self.path = f"{path}/instance{id}"
        self.get_public_and_private_keys()
        print(f"privateKey: {self._privateKey}, publicKey: {self._publicKey}")
        self.protocol_class = Protocol(self)
        self.nextAvailable = nextAvailable

    def get_public_and_private_keys(self):
        self._privateKey, self._publicKey = util.get_keys(self.path)
        if self._privateKey is None or self._publicKey is None:
            self._privateKey, self._publicKey = util.create_keys(self.path)

    def _create_protocol(self):
        return self.protocol_class

    def get_local_addr(self, node):
        return (node.host, node.port)

    async def bootstrap_node(self, mode):
        result = await self.protocol_class.ping(self.get_local_addr(mode), self._publicKey)
        #return Node(result[1], addr[0], addr[1]) if result[0] else None
        return None

    async def bootstrap(self, nodelist):
        cos = list(map(self.bootstrap_node, nodelist))
        gathered = await asyncio.gather(*cos)
        nodes = [node for node in gathered  if node is not None]

    async def listen_to_next_port(self):
        loop = asyncio.get_event_loop()
        while self.port < 65535:
            try: 
                listen = loop.create_datagram_endpoint(self._create_protocol,
                                               local_addr=self.get_local_addr(self))
                transport, protocol = await listen
                self.protocol_class.save_protocol_and_transport(protocol, transport)
                print(f"Node listening on {self.host}:{self.port}")
                return
            except OSError as e:
                self.port += 1
                if not self.nextAvailable:
                    return

    async def listen(self):
        await self.listen_to_next_port()
        #self.refresh_table()

    async def join(self, nodes=None):

        # listen
        print(f"Node::listen: host: {self.host}, port: {self.port}")
        await self.listen()

        if nodes is not None:
            print("Node::join existing...") 
            # bootstrap
            await self.bootstrap(nodes)
            
    def regenerateKey(self):
        print("Node::regenerateKey")

    def broadcast(self, message):
        print("Node::broadcast")
        return "OK"

    def count(self, message=None):
        print("Node::count")
        return 0
