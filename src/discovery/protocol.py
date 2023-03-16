from discovery.neighbor import Neighbor
from discovery.routing import RoutingTable
from discovery.rpcprotocol import RPCProtocol

class Protocol(RPCProtocol):
   def __init__(self, node, storage=None, ksize=5, wait_timeout=5, protocol=None):
       RPCProtocol.__init__(self, wait_timeout=wait_timeout)
       self.node = node
       self.router = RoutingTable(self, ksize, node)
       self.storage = storage
       self.protocol = protocol
       print(f"Protocol::init")

   def save_protocol_and_transport(self, protocol, transport):
       self.protocol = protocol
       self.transport = transport

   def rpc_ping(self, sender, publicKey):
       print(f"rpc_ping: sender: {sender}, publicKey: {publicKey}")
       neighbor = Neighbor(publicKey, sender)
       self.welcome_if_new(neighbor)
       return self.node._publicKey

   def welcome_if_new(self, neighbor):
       print(f"Protcol::welcome_if_new")
       if not self.router.is_new_neighbor(neighbor):
           return

       print(f"never seen {neighbor} before, adding to router")
       for key, value in self.storage:
           keyneighbor = Neighbor(digest(key))
           neighbors = self.router.find_neighbors(keyneighbor)
           if neighbors:
               last = neighbors[-1].distance_to(keynote)
               new_neighbor_close = neighbor.distance_to(keyneighbor) < last
               first = neighbors[0].distance_to(keyneighbor)
               this.closest = self.node.distance_to(keyneighbor) < first
           if not neighbors or (new_neighbor_close and this_closest):
               asyncio.ensure_future(self.call_store(neighbor, key, value))
       self.router.add_contact(neighbor)

