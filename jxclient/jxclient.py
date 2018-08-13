#!/usr/bin/env python

import ConfigParser, io, os, sys, getopt, pickle, socket, signal
from pprint import pprint

# Registering main root path for sane building!
sys.path.append(os.path.dirname(__file__))

from modules.transfer import *
from modules.utility import printLog

def usage():
    print 'jxclient -a|-h|-s|-p|-v'
    print '   -a <action>'
    print '      monitor:miner:cpu          Retrieving CPU miner log entry'
    print '      monitor:miner:gpu:x        Retrieving CPU miner x (0|1) log entry'
    print '      monitor:server:snapshot    Retrieving Full server logs non continuously'
    print '      monitor:server             Retrieving Full server logs in json format'
    print '      server:status              Checking server status'
    print '      server:shutdown            Shuts down the server'
    print '      server:reboot              Rebooting server instance'
    print '      server:update              Updating server loaded configuration'
    print '      config:load:json           Retrieving server configuration in json format'
    print '      config:save:json           Passing json to the server to be saved as config file'
    print '   -s Insert the server host ip address, default to 127.0.0.1'
    print '   -p Insert the server port number, default is 8129'
    print '   -j The json payload to be passed to the server'
    print '   -h Prints this help message'
    print '   -v Prints version'

def version():
    print '0.3.2'

def main():
    global t
    global soc

    action = ''
    payload = ''
    host = '127.0.0.1'
    port = 8129
    t = None
    soc = None

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Setup tools dont allow argument
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,"hi:vi:j:s:p:a:",["--action="])

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()

        if opt == '-v':
            version()
            sys.exit()

        if opt == '-s':
            host = str(arg)

        if opt == '-p':
            port = int(arg)

        if opt in ("-a", "--action"):
            action = arg

        if opt == '-j':
            payload = arg

    validActions = [
        'monitor:miner:cpu',
        'monitor:miner:gpu:0',
        'monitor:miner:gpu:1',
        'monitor:server:snapshot',
        'monitor:server',
        'server:status',
        'server:shutdown',
        'server:reboot',
        'server:update',
        'config:load:json',
        'config:save:json'
    ]

    if not action or action not in validActions:
        usage()
        sys.exit(2)

    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((host, port))
        printLog('Connected to --#%s#-:--#%s#-' % (host, port), 'success')

    except:
        printLog("Connection error", 'error')
        sys.exit()

    try:
        t = Transfer(soc)
        t.send(action)
        printLog('Sending --#%s#- action' % (action), 'success')

        if 'monitor' in action or 'config:load' in action:
            monitor(t)

        if 'config:save' in action:
            t.send(payload)

    except:
        printLog('Closing --#%s#- action' % (action), 'success')

    finally:
        shutdown()


def shutdown():

    if t:
        try:
            t.send('close')
            status = 'success'

        except:
            status = 'error'

        finally:
            printLog('Sending close action to server', status)

    if soc:
        try:
            soc.close()
            status = 'success'

        except:
            status = 'error'

        finally:
            printLog('Closing socket connection', status)

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
