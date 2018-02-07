import socket
import sys
import struct
import json
from helpers import mydir
from helpers import format_dirpath
from helpers import get_myip
from helpers import fix_ownership
import threading
from daemon2x import daemon
import time
import os


topdir = format_dirpath(mydir()+"../")
datadir = format_dirpath(topdir+"data/")
statedir = format_dirpath(topdir+"state/")
packetsdir = format_dirpath(datadir+"packets/")

cycle_time =  float(sys.argv[2])

dump_time = time.time() + cycle_time

myip = get_myip()

loc_port_map = dict()
with open(statedir+"port_loc_mapping.json", "r+") as f:
    loc_port_map = json.load(f)
myports = loc_port_map.values()


def update_dump_time(duration=None):
    global dump_time
    if duration is None:
        duration = cycle_time
    dump_time = time.time() + duration


def capture_packets():
    '''
    This page:
    http://www.binarytides.com/python-packet-sniffer-code-linux/
    significantly helped me get with handling raw packets, and has more details
    ---------------------
    create a AF_PACKET type raw socket (thats basically packet level)
    define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */
    '''
    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        s.settimeout(5) # force the loop to spin with a timeout
    except socket.error as msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    tvals = list()
    lastarr = 0.0
    # receive a packet
    while True:
        arr_time = time.time()
        # don't dump unless you're not currently serving
        if dump_time - arr_time <= 0 and arr_time - lastarr >= 5:
            print "dumping..."
            if len(tvals) > 0:
                fname = packetsdir + str(arr_time) + "_packets.json"
                with open(fname, "w+") as f:
                    json.dump(tvals, f)
                fix_ownership(fname)
                tvals = list()
            update_dump_time()
            print "dumped!"
        else:
            try:
                packet = s.recvfrom(65565)
            except socket.timeout:
                continue

            #packet string from tuple
            packet = packet[0]

            #parse ethernet header
            eth_length = 14

            eth_header = packet[:eth_length]
            eth = struct.unpack('!6s6sH' , eth_header)
            eth_protocol = socket.ntohs(eth[2])

            #Parse IP packets, IP Protocol number = 8
            if eth_protocol == 8 :
                #Parse IP header
                #take first 20 characters for the ip header
                ip_header = packet[eth_length:20+eth_length]

                #now unpack them :)
                iph = struct.unpack('!BBHHHBBH4s4s' , ip_header)

                version_ihl = iph[0]
                version = version_ihl >> 4
                ihl = version_ihl & 0xF

                iph_length = ihl * 4

                ttl = iph[5]
                protocol = iph[6]
                pdat = dict()
                pdat['s_ip'] = socket.inet_ntoa(iph[8]);
                pdat['d_ip'] = socket.inet_ntoa(iph[9]);

                #TCP protocol
                if protocol == 6 :
                    t = iph_length + eth_length
                    tcp_header = packet[t:t+20]

                    #now unpack them :)
                    tcph = struct.unpack('!HHLLBBHHH' , tcp_header)
                    pdat['s_port'] = tcph[0]
                    pdat['d_port'] = tcph[1]
                    pdat['seq'] = tcph[2]
                    pdat['ack'] = tcph[3]
                    pdat['flags'] = tcph[5]
                    pdat['cwnd'] = tcph[6]
                    pdat['time'] = arr_time
                    if (pdat['s_ip'] == myip and pdat['s_port'] in myports) or \
                            (pdat['d_ip'] == myip and pdat['d_port'] in myports):
                        print "adding to tvals..."
                        tvals.append(pdat)
                        lastarr = arr_time


class mydaemon(daemon):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        sys.stdout.flush()
        sys.stderr.flush()

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def run(self, **kwargs):
        sys.stdout.flush()
        sys.stderr.flush()
        os.chdir(topdir+"scripts/")
        capture_packets()


if __name__ == '__main__':
    pids_path = format_dirpath(statedir+'daemon/pids/')
    pidf = pids_path + 'sniff.pid'
    d = mydaemon(pidf)
    if 'start' == sys.argv[1]:
        d.start()
    elif 'stop' == sys.argv[1]:
        d.stop()
    elif 'restart' == sys.argv[1]:
        d.restart()
    elif 'status' == sys.argv[1]:
        d.status()
    elif 'v' == sys.argv[1]:
        d.run(no_daemon=True)
    else:
        raise ValueError('start/stop/restart/status/v list[ #]/download/scrape/full[ #]')
        sys.exit(2)
    sys.exit(0)
