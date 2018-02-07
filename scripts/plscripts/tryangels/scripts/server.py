# Most of the code in this file was acquired from
# It was modified for the needs of this project

#Packet sniffer in python
#For Linux - Sniffs all incoming and outgoing packets :)
#Silver Moon (m00n.silv3r@gmail.com)

from collections import defaultdict
import SocketServer, SimpleHTTPServer, BaseHTTPServer
import sys
from helpers import mydir
from helpers import format_dirpath
from helpers import get_myip
from helpers import fix_ownership
from daemon2x import daemon
import os


topdir = format_dirpath(mydir()+"../")
statedir = format_dirpath(topdir+"state/")


class req_handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    pass


class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


class mydaemon(daemon):
    def __init__(self, inport, pidfile, handler=None, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        sys.stdout.flush()
        sys.stderr.flush()

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.inport = int(inport)
        self.handler = handler

    def run(self):
        sys.stdout.flush()
        sys.stderr.flush()
        if self.handler is not None:
            Handler = self.handler
        else:
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = ThreadingHTTPServer(("",self.inport), Handler)
        try:
            os.chdir(topdir+"scripts/")
            httpd.serve_forever()

        except KeyboardInterrupt:
            httpd.shutdown()


if __name__ == '__main__':
    pids_path = format_dirpath(statedir+'daemon/pids/')
    pidf = pids_path + 'serv'+sys.argv[2]+'.pid'
    d = mydaemon(sys.argv[2], pidf)
    if 'start' == sys.argv[1]:
        d.start()
    elif 'stop' == sys.argv[1]:
        d.stop()
    elif 'restart' == sys.argv[1]:
        d.restart()
    elif 'status' == sys.argv[1]:
        d.status()
    elif 'v' == sys.argv[1]:
        d.run()
    else:
        raise ValueError('start/stop/restart/status/v list[ #]/download/scrape/full[ #]')
        sys.exit(2)
    sys.exit(0)
