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
