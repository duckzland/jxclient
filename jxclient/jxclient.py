#!/usr/bin/env python

import ConfigParser, io, os, sys, getopt, pickle, socket, signal
from pprint import pprint

# Registering main root path for sane building!
sys.path.append(os.path.dirname(__file__))

from modules.transfer import *
from modules.utility import printLog

def usage():
    print 'jxclient.py -a|-h'
    print '   -a <action>'
    print '      monitor:miner:cpu          Retrieving CPU miner log entry'
    print '      monitor:miner:gpu:x        Retrieving CPU miner x (0|1) log entry'
    print '      monitor:server             Retrieving Full server logs in json format'
    print '      server:status              Checking server status'
    print '      server:shutdown            Shuts down the server'
    print '      server:reboot              Rebooting server instance'
    print '      server:update              Updating server loaded configuration'
    print '   -h Prints this help message'

def main():
    action = ''
    format = ''

    # Setup tools dont allow argument
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,"hi:a:",["--action="])

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()

        elif opt in ("-a", "--action"):
            action = arg

    validActions = [
        'monitor:miner:cpu',
        'monitor:miner:gpu:0',
        'monitor:miner:gpu:1',
        'monitor:server',
        'server:status',
        'server:shutdown',
        'server:reboot',
        'server:update'
    ]

    if not action or action not in validActions:
        usage()
        sys.exit(2)

    try:
        host = "127.0.0.1"
        port = 8129
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((host, port))
        printLog('Connected to --#%s#-:--#%s#-' % (host, port))

    except:
        printLog("Connection error")
        sys.exit()

    try:
        t = Transfer(soc)
        t.send(action)
        printLog('Sending --#%s#- action' % (action))

        if 'monitor' in action:
            monitor(t)

    except:
        printLog('Closing --#%s#- action' % (action))

    finally:
        t.send('close')
        soc.close()
        printLog('Exiting client program', 'success')
        os._exit(1)



def monitor(t):
    while True:
        line = t.recv()
        if not line:
            break
        print(line.strip('\n'))


if __name__ == "__main__":
    main()
