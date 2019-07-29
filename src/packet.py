import copy
import pickle
from pprint import pprint


INFINITY = 16


class Packet(object):

    def __init__(self, command, routerId, payload, peer):
        self.version = 2
        self.command = command #always response only (no request for this assignment)
        self.routerId = routerId
        self.payload = payload
        self.peer = peer

    def makeHeader(self):
        return {'version': self.version, 'command': self.command, 'routerId': self.routerId}

    def makePayload(self):
        tableCopy = copy.deepcopy(self.payload.getTable())

        for dest, v in tableCopy.items():
            if self.peer == v['nextHop']:  # split-horizon w/ reverse poison
                v['metric'] = INFINITY

        return tableCopy

    def makeTriggerUpdatePayload(self):
        tableCopy = copy.deepcopy(self.payload.getTable())

        for k, v in list(tableCopy.items()):
            if v['routeChanged'] == False:
                tableCopy.pop(k)
            if self.peer == v['nextHop']:
                v['metric'] == INFINITY

        return tableCopy

    def makePacket(self, header, payload):
        packet = {}
        packet.update(header)
        packet.update(payload)
        picklePacket = pickle.dumps(packet)
        return picklePacket

    def sendPacket(self, packet, port, host, sockets):
        sockets[0].sendto(packet, (host, int(port)))
