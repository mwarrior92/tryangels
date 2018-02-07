from easiest.platform_libs import planet_lab as pl
from time import sleep
from easiest.helpers import mydir
import json

statedir = mydir()+"plscripts/tryangels/state/"
with open("auth.igme", "r+") as f:
    pw = json.load(f)
auth = {
        'Username': pl.config_data['planetlab_username'],
        'AuthString': pw[0],
        'AuthMethod': 'password'
        }
# auth = pl.create_auth()
'''
print "adding booted nodes"
pl.add_booted_nodes(auth)
#pl.drop_dead_nodes(auth)
print "refreshing added node list"
pl.refresh_added_node_list(auth)
print "refreshing usable nodes list"
pl.refresh_usable_nodes_list()

#print "sleeping"
#sleep(60*60*3)
'''

loc_port_map = dict()
with open(statedir+"port_loc_mapping.json", "r+") as f:
    loc_port_map = json.load(f)

print "setting up nodes"
methods = [pl.setup_python, pl.push_dir, pl.setup_sudoers, pl.execute_cmd]
snifferblob = mydir()+"plscripts/tryangels/"

startserv = "cd tryangels/scripts/"
startserv += "; sudo \
        \"LD_LIBRARY_PATH=$LD_LIBRARY_PATH\" python2.7 \
        sniffer.py start 60"
for p in loc_port_map.values():
    startserv += "; python2.7 server.py start "+str(p)
pl.setup_nodes(auth, setup_methods=methods, pushdir=snifferblob, cmd=startserv,
        max_nodes=1, remote_overwrite=True)
