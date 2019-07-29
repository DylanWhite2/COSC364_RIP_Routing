import json
from socket import *
import random
import time
import select
from pprint import pprint
from threading import *
import threading
import pickle
import copy
import table
from entry import *
from packet import *


HOST = '127.0.0.1'
INFINITY = 16
PERIOD = 10          #send periodic updates every 30 seconds to neighbour/peer routers.
TIMEOUT = PERIOD * 6 #start timeout timer after 180 seconds of not receiving an update
GARBAGE = PERIOD * 4 #start garbage collection 120 seconds after timeout has expired. (removes dead entries after 300 seconds)


class Router(object):

    def __init__(self, inputs, outputs, routerId):
        self.sockets = []
        self.inputPorts = inputs
        self.outputs = outputs
        self.routerId = routerId
        self.routeTable = table.RouteTable()
        self.time = 0
        self.randTime = random.randint(PERIOD - 5, PERIOD + 5)
        self.triggeredUpdateTimer = 0
        self.triggeredUpdatePeriod = random.randint(1, 5)
        self.peerRouters = []
        self.tableMutex = Lock()

        self.createSockets()
        self.createInitTable()
        self.getPeerRouters()

    def createSockets(self):
        for port in self.inputPorts:
            try:
                s = socket(AF_INET, SOCK_DGRAM)
                s.bind((HOST, int(port)))
                self.sockets.append(s)
                pprint('Opened socket on port: ' + str(port))
            except:
                pprint('Could not open socket on port: ' + str(port))

    def getPeerRouters(self):
        for output in self.outputs:
            output = output.split('-')
            self.peerRouters.append(output[2])

    def createInitTable(self):
        for output in self.outputs:
            output = output.split('-')
            entry = Entry(output[0], output[2], output[1],
                          self.routerId, output[2])
            entry = entry.createEntry()
            self.routeTable.addEntry(entry)

    def addFoundPeer(self, sourceId):
        for output in self.outputs:
            output = output.split('-')
            if output[2] == sourceId:
                entry = Entry(output[0], output[2],
                              output[1], self.routerId, output[2])
                entry = entry.createEntry()
                self.routeTable.addEntry(entry)

    def updateGlobalTimers(self):
        self.time += 1
        self.triggeredUpdateTimer += 1

    def updateTimeouts(self):
        # list makes a copy of the keys to avoid RuntimeError (dictionary changing size)
        for k in list(self.routeTable.getTable().keys()):
            garbageUpdated = False
            self.routeTable.updateTimeoutTimer(k)

            if self.routeTable.getRouteMetric(k) == INFINITY:
                self.routeTable.updateGarbageTimer(k)
                garbageUpdated = True

            if self.routeTable.getTimeoutTimer(k) >= TIMEOUT:
                oldMetric = self.routeTable.getRouteMetric(k)

                if oldMetric != INFINITY:
                    self.routeTable.updateRouteMetric(k, INFINITY)
                    self.routeTable.setRouteChangedFlag(k)

                if not garbageUpdated:
                    self.routeTable.updateGarbageTimer(k)

                if self.routeTable.getGarbageTimer(k) > GARBAGE:
                    self.routeTable.getTable().pop(k)

    def checkUpdateTimers(self):
        if self.time >= self.randTime:
            self.periodicUpdate()
            self.time = 0
            self.randTime = random.randint(PERIOD - 2, PERIOD + 2)

        # prevents sending triggered update if periodic is scheduled sooner
        if self.randTime - self.time < self.triggeredUpdateTimer - self.triggeredUpdatePeriod:
            self.triggeredUpdateTimer = 0

        if self.checkForTriggeredUpdates():
            if self.triggeredUpdateTimer >= self.triggeredUpdatePeriod:
                self.triggeredUpdate()
                self.routeTable.resetRouteChangedFlag()
                self.triggeredUpdateTimer = 0
                self.triggeredUpdatePeriod = random.randint(1, 5)

    def printTable(self):
        self.routeTable.printFormattedTable(self.routerId)

    def periodicUpdate(self):
        for output in self.outputs:
            output = output.split('-')
            port = output[0]
            peer = output[2]

            packet = Packet(2, self.routerId, self.routeTable,
                            peer)  # 2 == response (not required)
            header = packet.makeHeader()
            payload = packet.makePayload()
            packetToSend = packet.makePacket(header, payload)
            packet.sendPacket(packetToSend, port, HOST, self.sockets)

    def triggeredUpdate(self):
        for output in self.outputs:
            output = output.split('-')
            port = output[0]
            peer = output[2]

            packet = Packet(2, self.routerId, self.routeTable,
                            peer)  # 2 == response (not required)
            header = packet.makeHeader()
            payload = packet.makeTriggerUpdatePayload()
            packetToSend = packet.makePacket(header, payload)
            packet.sendPacket(packetToSend, port, HOST, self.sockets)

    def recv(self):
        readable, _, _ = select.select(self.sockets, [], [], 0)
        for s in readable:
            packet, _ = s.recvfrom(4096)
            loadedPacket = pickle.loads(packet)
            threading.Thread(target=self.processIncomingPacket(loadedPacket)).start()

    def validateIncomingPacket(self, packet):
        validPacket = True  # assume the packet is valid from the start

        testPacket = copy.deepcopy(packet)

        if testPacket['version'] != 2:
            validPacket = False

        if testPacket['command'] != 2:
            validPacket = False

        if testPacket['routerId'] not in self.peerRouters:
            validPacket = False

        testPacket.pop('version')
        testPacket.pop('command')
        testPacket.pop('routerId')

        for k, v in testPacket.items():
            if int(v['metric']) > INFINITY or int(v['metric']) < 1:
                validPacket = False

        if validPacket:
            return packet
        else:
            pprint('Invalid packet. Dropping...')
            return None

    def processIncomingPacket(self, packet):
        packet = self.validateIncomingPacket(packet)

        if packet is None: # Can be None if fails validity check
            return

        sourceId = packet['routerId'] #get the relavent header info then pop it
        packet.pop('version')
        packet.pop('command')
        packet.pop('routerId')

        self.tableMutex.acquire() #mutex to lock the route table because of multithreaded processing of incoming packets.

        try:
            # reestablishes a to a peer router if timed out
            if sourceId not in self.routeTable.getTable().keys():
                for output in self.outputs:
                    output = output.split('-')
                    if sourceId == output[2]:
                        self.addFoundPeer(sourceId)

            # for all RTEs in the incoming packet...
            for incomingDest, incomingValue in list(packet.items()):

                # for all entries in the current route table...
                for dest, values in self.routeTable.getTable().items():
                    # the next hop for this dest has sent a packet so reset timers
                    if self.routeTable.getNextHop(dest) == sourceId and self.routeTable.getRouteMetric(dest) != INFINITY:
                        self.routeTable.resetTimeoutTimer(dest)
                        self.routeTable.resetGargbageTimer(dest)
                    # if a peer router has timed out and reconnects, reinit the table with config file details
                    elif dest == sourceId and self.routeTable.getGarbageTimer(dest) > 0:
                        self.addFoundPeer(sourceId)

                # checking if the dest already exists in table. (Don't add itself to own route table)
                if incomingDest in self.routeTable.getTable().keys() and incomingDest != self.routerId:
                    newMetric = min(int(
                        incomingValue['metric']) + int(self.routeTable.getRouteMetric(sourceId)), INFINITY)

                    for dest, values in self.routeTable.getTable().items():
                        if incomingDest == dest:
                            # if the packet is from the current next hop, update the metric
                            if sourceId == self.routeTable.getNextHop(dest):
                                oldMetric = self.routeTable.getRouteMetric(dest)
                                self.routeTable.updateRouteMetric(dest, newMetric)
                                # if the route has been marked unreachable, set the flag for triggered update
                                if newMetric == INFINITY and oldMetric != INFINITY:
                                    self.routeTable.setRouteChangedFlag(dest)
                            else:
                                # if the packet is from a different next hop router, only change the next hop if the
                                # cost is lower.
                                if newMetric < int(self.routeTable.getRouteMetric(dest)):
                                    self.routeTable.updateNextHop(dest, sourceId)
                                    self.routeTable.updateRouteMetric(
                                        dest, newMetric)
                                    self.routeTable.resetTimeoutTimer(dest)
                                    self.routeTable.resetGargbageTimer(dest)


                # not in the table, add a new entry
                elif incomingDest not in self.routeTable.getTable().keys() and int(incomingValue['metric']) < INFINITY and incomingDest != self.routerId:
                    newMetric = min(int(
                        incomingValue['metric']) + int(self.routeTable.getRouteMetric(sourceId)), INFINITY)
                    entry = Entry(
                        incomingValue['port'], incomingDest, newMetric, sourceId, sourceId)
                    entry = entry.createEntry()
                    self.routeTable.addEntry(entry)
                    self.routeTable.resetTimeoutTimer(incomingDest)
                    self.routeTable.resetGargbageTimer(incomingDest)

        finally:
            self.tableMutex.release()

    def checkForTriggeredUpdates(self):
        updatesToSend = False
        for k, v in self.routeTable.getTable().items():
            if v['routeChanged'] == True:
                updatesToSend = True
        return updatesToSend

    def run(self):
        while(1):
            time.sleep(1)
            self.updateGlobalTimers()
            self.updateTimeouts()
            self.checkUpdateTimers()
            self.recv()
            self.printTable()
