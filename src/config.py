import json
from pprint import pprint
from collections import Counter
import sys


class Config(object):

    def __init__(self, configFile):
        self.configFile = configFile

        self.loadConfig()
        self.checkConfigParams()

    def loadConfig(self):
        try:
            with open(self.configFile) as configParams:
                configParams = json.load(configParams)
        except ValueError as e:
            pprint('Error parsing ' + str(self.configFile) +
                   ". Likely due to malformed JSON.")
            return False
        else:
            self.routerid = configParams['router-id']
            self.inputPorts = configParams['input-ports']
            self.outputs = configParams['outputs']
            return True

    def checkConfigParams(self):
        try:
            # router id checks
            if not self.routerid:
                raise AttributeError(
                    'Missing router ID. Check config file and restart.')
            if not self.routerid.isdigit():
                raise TypeError(
                    'RouterID Error. Check config file and restart.')

            # input ports checks
            inputPortCount = Counter(self.inputPorts)
            for port, occurences in inputPortCount.items():
                if occurences > 1:
                    raise ValueError(
                        'Multiple occurences of input ports. Check config file and restart')
            for port in self.inputPorts:
                if not str(port).isdigit():
                    raise ValueError(
                        'Input port(s) non-numerical. Check config file and restart.')
                if int(port) < 1024 or int(port) > 64000:
                    raise ValueError(
                        'Input port(s) out of range. Check config file and restart.')

            # output params checks
            outputPorts = []

            if not self.outputs:
                raise AttributeError(
                    'Missing output parameters. Check config file and restart.')
            for output in self.outputs:
                output = output.split('-')
                port = output[0]
                metric = output[1]
                peer = output[2]
                outputPorts.append(int(port))

                if not str(port).isdigit():
                    raise ValueError(
                        'Output port(s) non-numerical. Check config file and restart.')
                if int(port) < 1024 or int(port) > 64000:
                    raise ValueError(
                        'Output port(s) out of range. Check config file and restart.')
                if not str(metric).isdigit():
                    raise ValueError(
                        'Metric value(s) non-numerical. Check config file and restart.')
                if not str(peer).isdigit():
                    raise ValueError(
                        'Peer router value(s) non-numerical. Check config file and restart.')

            outputPortCount = Counter(outputPorts)
            for port, occurences in outputPortCount.items():
                if occurences > 1:
                    raise ValueError(
                        'Multiple occurences of output ports. Check config file and restart')

            if set(self.inputPorts) & set(outputPorts):
                raise ValueError(
                    'Cannot have same port for input and output. Check config file and restart.')

        except ValueError as e:
            pprint(str(e))
            sys.exit(0)
            return False
        except AttributeError as e:
            pprint(str(e))
            sys.exit(0)
            return False
        else:
            return True

    def getOutputs(self):
        return self.outputs

    def getInputs(self):
        return self.inputPorts

    def getRouterId(self):
        return self.routerid

    def getConfigParams(self):
        return self.inputPorts, self.outputs, self.routerid
