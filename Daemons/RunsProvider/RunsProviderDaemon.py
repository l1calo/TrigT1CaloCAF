#!/usr/bin/env python

import sys, time, os
from Daemon import Daemon
from RunsProvider import RunsProvider

class RunsProviderDaemon(Daemon):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/tmp/l1ccalib/std.txt', stderr='/tmp/l1ccalib/err.txt'):
        Daemon.__init__(self, pidfile, stdin, stdout, stderr)

    def run(self):
        #if not self.runsProvider.isInitialized():
        #   sys.exit(0)

        # the demaon chdir to '/' before the call to runtime_error
        # W0Monitor expect a local path to its config file, so we chdir to where
        # the config file is
        os.chdir(os.environ["PWD"])
        self.runsProvider = RunsProvider("RunsProviderConfig.py")
        #os.chdir('/')

        #sys.stdout.flush()
        #sys.stderr.flush()

        while True:
            time.sleep(900)
            #time.sleep(120)
            #time.sleep(30)
            
            self.runsProvider.listen()

            #sys.stdout.flush()
            #sys.stderr.flush()

if __name__ == "__main__":
    daemon = RunsProviderDaemon(os.environ["PWD"]+'/runsproviderdaemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
