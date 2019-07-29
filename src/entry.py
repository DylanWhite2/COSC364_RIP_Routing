from pprint import pprint


class Entry(object):

    def __init__(self, nextPort, dest, metric, parent, nextHop):
        self.nextPort = nextPort
        self.dest = dest
        self.metric = metric
        self.parent = parent
        self.nextHop = nextHop
        self.timeoutTimer = 0
        self.garbageTimer = 0
        self.routeChanged = False
        self.entry = {}

    def createEntry(self):
        self.entry[self.dest] = {
            'metric': self.metric,
            'nextHop': self.nextHop,
            'parent': self.parent,
            'port': self.nextPort,
            'timeout': self.timeoutTimer,
            'garbage': self.garbageTimer,
            'routeChanged': self.routeChanged,
        }
        return self.entry.items()

    def printEntry(self):
        pprint(self.entry)
