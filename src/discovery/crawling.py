from discovery.util import gather_dict
from discovery.nodeheap import NodeHeap
from discovery.rpcfindresponse import RPCFindResponse


class SpiderCrawl:
    def __init__(self, protocol, node, peers, ksize, alpha):
        self.protocol = protocol
        self.ksize = ksize
        self.alpha = alpha
        self.node = node
        self.nearest = NodeHeap(self.node, self.ksize)
        self.last_ids_crawled = []
        self.nearest.push(peers)

    async def _find(self, rpcmethod):
        count = self.alpha
        if self.nearest.get_ids() == self.last_ids_crawled:
            count = len(self.nearest)
        self.last_ids_crawled = self.nearest.get_ids()

        dicts = {}
        for peer in self.nearest.get_uncontacted()[:count]:
            dicts[peer.id] = rpcmethod(peer, self.node)
            self.nearest.mark_contacted(peer)
        found = await gather_dict(dicts)
        return await self._nodes_found(found)

class NodeSpiderCrawl(SpiderCrawl):
    async def find(self):
        return await self._find(self.protocol.call_find_node)

    async def _nodes_found(self, responses):
        toremove=[]
        for peerid, response in responses.items():
            response = RPCFindResponse(response)
            if not response.happened():
                toremove.append(peerid)
            else:
                self.nearest.push(response.get_node_list())
        self.nearest.remove(toremove)

        if self.nearest.have_contacted_all():
            return list(self.nearest)
        return await self.find()

