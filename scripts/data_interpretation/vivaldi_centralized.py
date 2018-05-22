import math, random, time
from util import *

class Network:
    def __init__(self, rtt_data):
        #rtt_data is a dictionary of dictionaries containing RTT between two ips
        # EX rtt_data[10.10.10.1][10.10.10.2] = 0.04
        # assumes each ip has an RTT with each other ip

        num_ips = len(rtt_data.keys())
        ip_to_idx = {}
        ips = rtt_data.keys()
        for i in xrange(num_ips):
            ip_to_idx[ips[i]] = i



        self.latency_matrix = [[x for x in xrange(0,num_ips)] for y in xrange(0,num_ips)]

        for n in xrange(num_ips):
            for m in xrange(num_ips):
                self.latency_matrix[n][m] = rtt_data[ips[n]][ips[m]]

        self.nodes = [Point() for x in xrange(0,num_ips)]

    def __str__(self):
        s = ""
        for c in self.nodes:
            s += str(c)+"\n"

        return s


    def centralized_vivaldi(self, stall=1, thresh=0.1, ts=0.5):
        n = len(self.nodes)
        same_count = 0
        err = 0
        rnd = 0
        while same_count < stall:
            #print "Round: ", rnd
            rnd += 1
            new_err = total_error(self.latency_matrix, self.nodes)
            #print new_err, err
            if new_err < err+thresh and new_err > err-thresh:
                same_count += 1
            else:
                same_count = 0
            err = new_err

            #print total_error(latency_mat, coords)
            for i in xrange(0,n):
                f = Point(0,0)
                for j in xrange(0, n):
                    if i == j:
                        continue
                    n1 = self.nodes[i]
                    n2 = self.nodes[j]
                    e = self.latency_matrix[i][j] - dist(n1, n2)
                    unit_vec = n1 - n2
                    unit_vec = unit_vec.unit()
                    f = f + unit_vec.mult_const(e)
                self.nodes[i] = self.nodes[i] + f.mult_const(ts)

            #for c in self.nodes:
            #    print c, "\n"
            #time.sleep(1)

    def experiment():
        return



if __name__ == "__main__":
    #print "Make a blank network"
    #d = {}
    #n = Network(d)
    #print n

    #print "Run vivaldi"
    #n.centralized_vivaldi()
    #print n

    #import pickle

    #with open("rtt_data.p", "rb") as f:
    #    data = pickle.load(f)

    #print len(data.keys())
    #s = {}
    #for k in data.keys():
    #    s[k] = 1


    #rtts = []
    #for k in data.keys():
    #    for kk in data[k].keys():
    #        if data[k][kk] == 0:
    #            print k, kk
    #        rtts.append(data[k][kk])

    #print max(rtts), min(rtts)

    fake_data = {"10.10.10.1": {"10.10.10.2": 0.02, "10.10.10.1": 0.0}, "10.10.10.2": {"10.10.10.1": 0.03, "10.10.10.2": 0}}

    n = Network(fake_data)
    print n, n.latency_matrix
