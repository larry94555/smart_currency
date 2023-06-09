# first node

import argparse
import asyncio
import logging
from discovery.message import Message
from discovery.server import Server

# Actions
#--------
# 1. Listen
# 2. Handle Incoming Requests
#    2a. Join -- accept a node to the network
#    2b. Broadcast -- receive a message
#    2c. Count -- count how many nodes have received a message and how many
#                 nodes exist.

# Design
#-------
# 1. The application should be trivial and leverage the existing library.
# 2. The logic should implement the actions only
#

def parse_arguments():
    """
    -bp, --baseport: the starting port to use
    -h, --host: the host to use for all nodes on this ip address
    -nc, --nodecount: specify the number of nodes to start with
    -pa, --path: specify the path for directory, private key, tc.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-bp", "--baseport", help="starting port to use", type=int, default=3000)
    parser.add_argument("-ho", "--host", help="specify the host to use", type=str, default="127.0.0.1")
    parser.add_argument("-nc", "--nodecount", help="number of nodes to bootstrap", type=int, default=1)
    parser.add_argument("-pa", "--path", help="specify the path for directory", type=str, default="test")
    return parser.parse_args()
    
async def main(loop):
    """
    bootstrap nc nodes which is used to test out the library.
    """
    args = parse_arguments()
    loop = asyncio.new_event_loop()
    #loop = asyncio.get_event_loop()
    bp = args.baseport
    ho = args.host
    nc = args.nodecount
    p = args.path
    
    s = "" if args.nodecount == 1 else "s"
    print(f"Initiating {nc} node{s}...")
    firstServer = Server(id=0, host=ho, port=bp, path=p)
    first = await firstServer.join()
    servers = [firstServer]
    port=bp+1
    if nc > 1:
        for i in range(nc-1):
            print(f"\n\nmain::loop: i={i}")
            server = Server(id=i+1, host=ho, port=port)
            port = server.port + 1
            await server.join(servers)
            servers.append(server)
    message = Message("Test")
    result=firstServer.broadcast(message)
    count = firstServer.count(message) 
    total = firstServer.count()
    print(f"Sent message:{message.getSubject()} to {count} servers out of total: {total}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(loop))
    #loop.run_forever()

