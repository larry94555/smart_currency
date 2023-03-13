import asyncio
from base64 import b64encode
from discovery.exceptions import MalformedMessage
import os
from hashlib import sha1
import umsgpack

class RPCProtocol(asyncio.DatagramProtocol):
    def __init__(self, wait_timeout=5):
        print(f"RPCProtocol::init")
        self._wait_timeout = wait_timeout
        self._outstanding = {}
        self.transport = None

    def connection_made(self, transport):
        print(f"connection_made")
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f"datagram_received: addr: {addr}")
        asyncio.ensure_future(self._solve_datagram(data, addr))

    async def _solve_datagram(self, datagram, address):
        if len(datagram) < 22:
             print(f"received datagram too small from {address} ignoring")
             return

        msg_id = datagram[1:21]
        data = umsgpack.unpackb(datagram[21:])
        if datagram[:1] == b'\x00':
            asyncio.ensure_future(self._accept_request(msg_id, data, address))
        elif datagram[:1] == b'\x01':
            self._accept_response(msg_id, data, address)
        else:
            print(f"Received unknown message from {address}, ignoring")

    async def _accept_request(self, msg_id, data, address):
        if not isinstance(data, list) or len(data) != 2:
            raise MalformedMessage(f"Could not read packet: {data}") 
        funcname, args = data
        func = getattr(self, "rpc_%s" % funcname, None)
        if func is None or not callable(func):
            msgargs = (self.__class__, __name__, funcname)
            print("%s has no callable method "
                  "rpc_%s; ignoring request", *msgargs)
            return
        
        if not asyncio.iscoroutinefunction(func):
            func = asyncio.coroutine(func)
        response = await func(address, *args)
        print(f"sending response {response} for msg id {b64encode(msg_id)} to {address}")
        txdata = b'\x01' + msg_id + umsgpack.packb(response)
        self.transport.sendto(txdata, address)

    def _accept_response(self, msg_id, data, address):
        msgargs = (b64encode(msg_id), address)
        if msg_id not in self._outstanding:
            print("received unknown message %s "
                  "from %s; ignoring", *msgargs)
            return
        print("received response %s for message "
              "id %s from %s", data, *msgargs)
        future, timeout = self._outstanding[msg_id]
        timeout.cancel()
        future.set_result((True, data))
        del self._outstanding[msg_id]

    def _timeout(self, msg_id):
        args = (b64encode(msg_id), self._wait_timeout)
        self._outstanding[msg_id][0].set_result((False, None))
        del self._outstanding[msg_id]

    def __getattr__(self, name):
        if name.startswith("_") or name.startswith("rpc_"):
            return getattr(super(), name)
        
        try:
            return getattr(super(), name)
        except AttributeError:
            pass

        def func(address, *args):
            msg_id = sha1(os.urandom(32)).digest()
            data = umsgpack.packb([name, args])
            if len(data) > 8192:
                raise MalformedMessage(f"Total length of function "
                                       f"name and arguments cannot exceed 8K")
            txdata = b'\x00' + msg_id + data
            self.transport.sendto(txdata, address)
            loop = asyncio.get_event_loop()
            if hasattr(loop, 'create_future'):
                future =loop.create_future()
            timeout = loop.call_later(self._wait_timeout,
                                      self._timeout, msg_id)
            self._outstanding[msg_id] = (future, timeout)
            return future
        return func

