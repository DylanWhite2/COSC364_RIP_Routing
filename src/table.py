from pprint import pprint

WIDTH = 13
INFINITY = 16

LINE = ('+' + ''.center(WIDTH, '-') +
        '+' + ''.center(WIDTH, '-') +
        '+' + ''.center(WIDTH, '-') +
        '+' + ''.center(WIDTH, '-') +
        '+' + ''.center(WIDTH, '-') +
        '+' + ''.center(WIDTH, '-') +
        '+')

class RouteTable(object):

    def __init__(self):
        self.table = {}

    def addEntry(self, entry):
        self.table.update(entry)

    def removeEntry(self, dest):
        self.table.pop(dest)

    def getEntry(self, dest):
        return self.table[dest]

    def getTable(self):
        return self.table

    def getRouteMetric(self, dest):
        return self.table[dest]['metric']

    def getTimeoutTimer(self, dest):
        return self.table[dest]['timeout']

    def getGarbageTimer(self, dest):
        return self.table[dest]['garbage']

    def getNextHop(self, dest):
        return self.table[dest]['nextHop']

    def updateRouteMetric(self, dest, metric):
        self.table[dest]['metric'] = metric
        return metric

    def updateNextHop(self, dest, nextHop):
        self.table[dest]['nextHop'] = nextHop

    def updateTimeoutTimer(self, dest):
        timeoutTimer = self.getTimeoutTimer(dest)
        newTime = timeoutTimer + 1
        timeout = {'timeout': newTime}
        self.table[dest].update(timeout)

    def updateGarbageTimer(self, dest):
        garbageTimer = self.getGarbageTimer(dest)
        newTime = garbageTimer + 1
        garbage = {'garbage': newTime}
        self.table[dest].update(garbage)

    def setRouteChangedFlag(self, dest):
        self.table[dest]['routeChanged'] = True

    def resetTimeoutTimer(self, dest):
        self.table[dest]['timeout'] = 0

    def resetGargbageTimer(self, dest):
        self.table[dest]['garbage'] = 0

    def resetRouteChangedFlag(self):
        for k, v in self.table.items():
            if v['routeChanged'] == True:
                v['routeChanged'] = False

    def printTable(self):
        pprint(self.table)

    def printFormattedTable(self, routerId):
        print('Table of Router : {}'.format(routerId).center(80, ' '))
        print(LINE)
        print('|' + 'Dest'.center(WIDTH, ' ') +
              '|' + 'Cost'.center(WIDTH, ' ') +
              '|' + 'Next Hop'.center(WIDTH, ' ') +
              '|' + 'Timeout'.center(WIDTH, ' ') +
              '|' + 'Garbage'.center(WIDTH, ' ') +
              '|' + 'Route Changed'.center(WIDTH, ' ') +
              '|')
        print(LINE)
        for k, v in sorted(self.table.items()):
            print('|' + str(k).center(WIDTH, ' ') +
                  '|' + str(v['metric']).center(WIDTH, ' ') +
                  '|' + str(v['nextHop']).center(WIDTH, ' ') +
                  '|' + str(v['timeout']).center(WIDTH, ' ') +
                  '|' + str(v['garbage']).center(WIDTH, ' ') +
                  '|' + str(v['routeChanged']).center(WIDTH, ' ') +
                  '|')
        print(LINE)
        print(' ')
