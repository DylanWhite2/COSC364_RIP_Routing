#!/usr/bin/python3

from config import *
from router import *
import threading
import sys


def main():
    config = Config(sys.argv[1])
    inputs, outputs, routerId = config.getConfigParams()

    router = Router(inputs, outputs, routerId)
    threading.Timer(1.0, router.run()).start() #start the daemon


if __name__ == '__main__':
    main()
