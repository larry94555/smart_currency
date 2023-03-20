import asyncio
from discovery.storage import ForgetfulStorage
from discovery.node import Node
from discovery.protocol import Protocol
from discovery.crawling import NodeSpiderCrawl
import discovery.util as util

class Server:
    """
    Main class that handles the following features:
    1.  Join
    2.  Broadcast
    3.  Count
    4.  Regenerate Key
    """

    def __init__(self, id=0, host="127.0.0.1", port=1024, path="./test", storage=None, ksize=5, alpha=3, nextAvailable=True):
        print(f"Server::init: id: {id}, port: {port}")
        self.id = id
        self.host = host
        self.ksize = ksize
        self.alpha = alpha
        self.storage = storage or ForgetfulStorage()
        self.port = port
        self.path = f"{path}/instance{id}"
        self.get_public_and_private_keys()
        #print(f"privateKey: {self._privateKey}, publicKey: {self._publicKey}")
        self.protocol_class = Protocol(self, self.storage, self.ksize) 
        self.nextAvailable = nextAvailable

    def get_public_and_private_keys(self):
        self._privateKey, self._publicKey = util.get_keys(self.path)
        if self._privateKey is None or self._publicKey is None:
            util.create_keys(self.path)
            self._privateKey, self._publicKey = util.get_keys(self.path)

    def _create_protocol(self):
        return self.protocol_class

    def get_local_addr(self, server):
        return (server.host, server.port)

    def create_node(self):
        sender = (self.host, self.port)
        return Node(self._publicKey, sender)

    async def bootstrap_node(self, server):
        result = await self.protocol_class.ping(self.get_local_addr(server), self._publicKey)
        print(f"Server::bootstrap_server: received result: {result[0]} with id: {result[1]}")
        return Node(result[1], (server.host, server.port)) if result[0] else None

    async def bootstrap(self, serverlist):
        print(f"Server::bootstrap")
        cos = list(map(self.bootstrap_node, serverlist))
        gathered = await asyncio.gather(*cos)
        nodes = [node for node in gathered  if node is not None]
        spider = NodeSpiderCrawl(self.protocol_class, self.create_node(), nodes,
                                 self.ksize, self.alpha)
        return await spider.find()

    async def listen_to_next_port(self):
        loop = asyncio.get_event_loop()
        while self.port < 65535:
            try: 
                listen = loop.create_datagram_endpoint(self._create_protocol,
                                               local_addr=self.get_local_addr(self))
                transport, protocol = await listen
                self.protocol_class.save_protocol_and_transport(protocol, transport)
                print(f"Server::listen_to_next_port: listening on {self.host}:{self.port}")
                return
            except OSError as e:
                self.port += 1
                if not self.nextAvailable:
                    return

    async def listen(self):
        print(f"Server::listen")
        await self.listen_to_next_port()
        # spread table information
        #self.refresh_table()

    async def join(self, servers=None):

        # listen
        print(f"Server::join: host: {self.host}, port: {self.port}")
        await self.listen()

        if servers is not None:
            print(f"Server::join existing:server count: {len(servers)} ...") 
            # bootstrap
            await self.bootstrap(servers)
            
    def regenerateKey(self):
        print("Server::regenerateKey")

    def broadcast(self, message):
        print("Server::broadcast")
        return "OK"

    def count(self, message=None):
        print("Server::count")
        return 0
