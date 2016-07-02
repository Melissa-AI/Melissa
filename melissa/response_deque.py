# http://stackoverflow.com/questions/27345332/process-vs-thread-with-regards-to-using-queue-deque-and-class-variable-for

from multiprocessing.managers import SyncManager
from collections import deque

SyncManager.register('deque', deque)

def Manager():
    m = SyncManager()
    m.start()
    return m

class RD:
    class __RD:
        def __init__(self):
            self.m = Manager()
            self.q = self.m.deque()

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not RD.instance:
            RD.instance = RD.__RD()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def append(self, item):
        RD.instance.q.append(item)

    def popleft(self):
        return RD.instance.q.popleft()

    def getvalue(self):
        return RD.instance.q._getvalue()
