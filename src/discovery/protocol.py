from discovery.rpcprotocol import RPCProtocol

class Protocol(RPCProtocol):
   def __init__(self, node, wait_timeout=5, protocol=None):
       RPCProtocol.__init__(self, wait_timeout=wait_timeout)
       self.node = node
       self.protocol = protocol
       print(f"Protocol::init")

   def save_protocol_and_transport(self, protocol, transport):
       self.protocol = protocol
       self.transport = transport

   def rpc_ping(self, sender, nodeid):
       print(f"rpc_ping: sender: {sender}, nodeid: {nodeid}")
       #source = Node(nodeid, sender[0], sender[1])
       #self.welcome_if_new(source)
       #return self.source_node.id
       return None

