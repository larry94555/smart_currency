import operator
from collections import OrderedDict
from itertools import takewhile
import time

class ForgetfulStorage:
    def __init__(self, ttl=604800):
        self.data = OrderedDict()
        self.ttl = ttl

    def cull(self):
        for _, _ in self.iter_older_than(self.ttl):
            self.data.popitem(last=False)

    def iter_older_than(self, seconds_old):
        minBirthday = time.monotonic() - seconds_old
        zipped = self._triple_iter()
        matches = takewhile(lambda r: minBirthday >= r[1], zipped)
        return list(map(operator.itemgetter(0, 2), matches))

    def __iter__(self):
        self.cull()
        ikeys = self.data.keys()
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ivalues)

    def _triple_iter(self):
        ikeys = self.data.keys()
        ibirthday = map(operator.itemgetter(0), self.data.values())
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ibirthday, ivalues)
