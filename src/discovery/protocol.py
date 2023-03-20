from discovery.node import Node
from discovery.routing import RoutingTable
from discovery.rpcprotocol import RPCProtocol

class Protocol(RPCProtocol):
   def __init__(self, server, storage=None, ksize=5, wait_timeout=5, protocol=None):
       RPCProtocol.__init__(self, wait_timeout=wait_timeout)
       self.server = server
       self.node = server.create_node()
       self.router = RoutingTable(self, ksize, self.node)
       self.storage = storage
       self.protocol = protocol
       print(f"Protocol::init")

   def save_protocol_and_transport(self, protocol, transport):
       self.protocol = protocol
       self.transport = transport

   def rpc_find_node(self, sender, id, key):
       print(f"Protocol::rpc_find_neighbor")
       source = Node(id, sender)
       self.welcome_if_new(source)
       node = Node(key)
       nodes = self.router.find_neighbors(node, exclude=source)
       return list(map(tuple, nodes))

   def rpc_find_value(self, sender, nodeid, key):
       print(f"Protocol::rpc_find_value")
       source = Node(nodeid, sender)
       self.welcome_if_new(source)
       value = self.storage.get(key, None)
       if value is None:
           return self.rpc_find_node(sender, nodeid, key)
       return { 'value': value}

   async def call_find_value(self, node_to_ask, node_to_find):
       print(f"Protocol::call_find_value")
       address = neighbor_to_ask.sender
       result = await self.find_node(address, self.source)
       return self.handle_call_response(result, node_to_ask)

   async def call_ping(self, node_to_ask):
       print(f"Protocol::call_ping: node_to_ask: {node_to_ask.sender}, node port: {self.node.sender[1]}")
       address = node_to_ask.sender
       result = await self.ping(address, self.node.id)
       print(f"Protocol::call_ping: after await...")
       return self.handle_call_response(result, node_to_ask)

   def rpc_ping(self, sender, id):
       print(f"Protocol::rpc_ping: sender: {sender}, id: {id}")
       node = Node(id, sender)
       self.welcome_if_new(node)
       return self.node.id

   def welcome_if_new(self, node):
       print(f"Protcol::welcome_if_new: node: {node.id}")
       if not self.router.is_new_node(node):
           return

       print(f"Protocol::welcome_if_new: found new node: {node.id}, adding to router")
       for key, value in self.storage:
           print("iterating: key: {key}, value: {value}")
           keynode = Node(digest(key))
           neighbors = self.router.find_neighbors(keynode)
           if neighbors:
               last = neighbors[-1].distance_to(keynote)
               new_node_close = node.distance_to(keynode) < last
               first = neighbors[0].distance_to(keynode)
               this.closest = self.node.distance_to(keynode) < first
           if not neighbors or (new_node_close and this_closest):
               asyncio.ensure_future(self.call_store(node, key, value))
       self.router.add_contact(node)

   def handle_call_response(self, result, node):
       print(f"Protocol::handle_call_response")
       if not result[0]:
           print(f"Protocol::handle_call_response: no response from {node.port}, removing from router")
           self.router.remove_contact(node)
           return result
       print(f"Protocol::handle_call_response: got successful response from {node.port}")
       self.welcome_if_new(node)
       return result


