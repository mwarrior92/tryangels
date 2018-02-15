from easiest.platform_libs import planet_lab as pl
from time import sleep
from easiest.helpers import mydir
from easiest.helpers import format_dirpath
import json
import time
from random import shuffle

statedir = mydir()+"plscripts/tryangels/state/"
datadir = format_dirpath(mydir()+"../data/planet_lab/")
with open("auth.igme", "r+") as f:
    pw = json.load(f)
auth = {
        'Username': pl.config_data['planetlab_username'],
        'AuthString': pw[0],
        'AuthMethod': 'password'
        }

nodes = pl.get_nodes()

'''
#######################
print "getting IP to node mapping"
ips = dict()
for node in nodes:
    ip = pl.get_node_ip(node)
    print ip
    if ip is not None:
        ips[ip] = node

fname = datadir+"ip2node_"+str(time.time()).split('.')[0]+".json"
with open(fname, 'w+') as f:
    json.dump(ips, f)
'''

###################
print "beginning experiment..."
while True:
    started = time.time()
    for i, ni in enumerate(nodes):
        since_sleep = 0
        for nj in nodes:
            if nj != ni:
                print ni, nj
                success = pl.command_node(nj, "wget "+ni+":42000/networks_40x40.png; rm networks_40x40.png")
                if since_sleep > 14:
                    print "sleeping..."
                    time.sleep(60)
                    since_sleep = 0
                else:
                    since_sleep += 1
        print "sleeping..."
        time.sleep(126)

    shuffle(nodes)


