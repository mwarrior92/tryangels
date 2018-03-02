import json
import re, os
from ServerClientTuple import ServerClientTuple

#This file contains functions for reading in data from the json files
#and formatting them correctly. Space to add any other formatting options
#Also contains functions for adding inter packet gap and group by port (location)

def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data


def group_by_ip_pairs(data, serverIP):
    ips = [p['s_ip'] for p in data if p['s_ip'] != serverIP]
    ips += [p['d_ip'] for p in data if p['d_ip'] != serverIP]
    ips = list(set(ips))

    pairs = []

    for i in ips:
        packets = []
        for d in data:
            if (d['s_ip'] == serverIP and d['d_ip'] == i) or (d['d_ip'] == serverIP and d['s_ip'] == i):
                packets.append(d)
        pairs.append(ServerClientTuple(serverIP, i, packets))

    return pairs


def get_ip(dirname):
    matchObj = re.match( r'/?ip(\d+.\d+.\d+.\d+)', dirname)

    if matchObj:
        #print matchObj.group(1)
        return matchObj.group(1)
    else:
        print "Couldn't get IP"


def load_one_dir(dirname):
    serverIP = get_ip(dirname)

    pairs = []
    print dirname
    for root, dirs, files in os.walk(os.path.join("packets/", dirname)):
        for f in files:
            data = load_json(os.path.join("packets/", dirname+"/", f))
            pairs += group_by_ip_pairs(data, serverIP)
        break

    return pairs

def print_one_file(fname):
    with open(fname, 'r') as f:
        data = json.load(f)

    template = "S_IP: %s\nD_IP: %s\nTime: %s\nSeq: %s\nAck: %s\nFlags: %s\n"

    for d in data:
        print template % (d['s_ip'], d['d_ip'], d['time'], d['seq'], d['ack'], d['flags'])

def load_all(root_dir):
    data = {}
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            data[d] = load_one_dir(d)
        break

    return data
