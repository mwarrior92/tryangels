"""
To remind you what the nature of the experiment is: we're trying to build
"constraints" based on network information, such that we easily mark certain
geographic locations as "impossible", with the end goal being to make it
difficult to tell any significant lies about one's (mobile device's) location.

The code I used to deploy to the planet lab nodes is here:
https://github.com/mwarrior92/tryangels and https://github.com/mwarrior92/easiest
The main thing I would like you to look at is:
https://github.com/mwarrior92/tryangels/blob/master/scripts/plscripts/tryangels/scripts/sniffer.py

captures packet data and dumps it to json files
Assume that each port number pertains to a different client location I know in advance
(in other words, I'll only send clients from city A to port A).

You can make a sub-directory in tryangels/scripts for your work.
Push everything to the repo. We'll schedule a meeting soon.
It's okay if you get stuck, but continue to keep me posted on your progress.

NOTES

Packet Data Summary
pdat['s_ip'] = source IP address
pdat['d_ip'] = destination IP address
pdat['s_port'] = source port
pdat['d_port'] = destination port
pdat['seq'] = sequence number
pdat['ack'] = ack number
pdat['flags'] = flags (URG,ACK,PSH,RST,SYN,FIN)
pdat['cwnd'] = window size
pdat['time'] = time of arrival


ACK 'tcp[13] & 16 != 0'
SYN 'tcp[13] & 2 != 0'
FIN 'tcp[13] & 1 != 0'
URG 'tcp[13] & 32 != 0'
PSH 'tcp[13] & 8 != 0'
RST 'tcp[13] & 4 != 0'

Inferred features
inter-packet gap = difference between arrival times
avg number of resent packets = count number of packets with same seq and ack #
"""


"""
@TODO: write code to identify what features of the data (inter-packet gap, window size,
avg # resent packets, etc) most drastically/accurately distinguish locations

Approach:
First, group all packets by port (i.e. location)
Then, for each piece of data in the packet, examine them across all ports.

"""




"""
@TODO: write code for clustering (or labeling / categorizing) data
(for example, see if you use some features to group the data, and see how well
do those groups align with location information)
"""

"""
@TODO: write code to identify what features are the biggest sources of noise
"""


if __name__ == '__main__':
    from loading_and_processing import *
    import pickle
    #print_one_file("packets/ip128.8.126.79/t1518636333.83.json")


    #pairs = load_one_dir("ip128.10.18.52")
    #s, d = make_pair_rtt_dict(pairs)
    #print d
    #print s

    data = load_all("packets")

    with open("rtt_data.p", "w") as f:
        pickle.dump(data, f)
    #print len(pairs)
    #for i in pairs:
    #    continue
    #    print i, "\n"

    #d = load_all("packets")

    #print len(d.keys())
