import asyncio

class RPCProtocol(asyncio.DatagramProtocol):
    def __init__(self, wait_timeout):
        print(f"RPCProtocol::init")

    def connection_made(self, transport):
        self.transport = transport
