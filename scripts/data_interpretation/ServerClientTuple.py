#a class to represent each location
from operator import itemgetter

class ServerClientTuple:

    def __init__(self, server, client, l=[]):
        self.server = server
        self.client = client

        self.listOfPackets = sorted(l, key=itemgetter('time'))

        self.packetTimeDiff = 0
        self.calculatePacketTimeDiff()
        self.numResent = 0
        self.findNumResent()
        self.RTT = 0
        self.calculateRTT()
        self.name = ""

    def __str__(self):
        s = "Server: %s\nClient: %s\nRTT: %s\nPTD: %s\nNR: %s\n" % (self.server, self.client, self.RTT, self.packetTimeDiff, self.numResent)
        return s

    def calculatePacketTimeDiff(self):
        #assumes the packets are sorted by time of arrival
        gaps = []
        for i in xrange(len(self.listOfPackets)-1):
            #print self.listOfPackets[i+1]['time']
            #print self.listOfPackets[i]['time']
            gaps.append(self.listOfPackets[i+1]['time'] - self.listOfPackets[i]['time'])

        self.packetTimeDiff = sum(gaps) / float(len(gaps)) if len(gaps) > 0 else 0

    def findNumResent(self):
        resent = {}
        for p in self.listOfPackets:
            #cantor pairing function to make ack and seq a unique pair to hash for the dicitonary
            key = 0.5*(p['seq']+p['ack'])*(p['seq']+p['ack']+1) + p['ack']

            if resent.has_key(key):
                resent[key] += 1
            else:
                resent[key] = 0

        values = [resent[k] for k in resent.keys() if resent[k] > 0]

        self.numResent = sum(values)/float(len(values)) if len(values) > 0 else 0


    def calculateRTT(self):
        '''
        Find the first packet that is data (i.e. not a syn, synack, etc.) and record
        its sequence number. Then, find the next packet that is acking that sequence number
        '''

        rtts = []

        #find the packets that aren't syns
        for p1 in xrange(len(self.listOfPackets)):
            if self.listOfPackets[p1]['flags'] == 24 and self.listOfPackets[p1]['s_ip'] == self.server: #if it is a data packet, ACK(16) and PSH(8) flags
                ack = self.listOfPackets[p1]['ack']
                #record the seq, and look for the packet that acks it
                for p2 in xrange(p1+1, len(self.listOfPackets)):
                    if self.listOfPackets[p2]['seq'] == (ack) and self.listOfPackets[p2]['d_ip'] == self.server:
                        rtts.append(self.listOfPackets[p2]['time'] - self.listOfPackets[p1]['time'])
                        break

        self.RTT = sum(rtts) / float(len(rtts)) if len(rtts) > 0 else 0


    def addPackets(self, packets):
        '''
        adds one or more packets to the class, assumes packets is a list of one
        or more elements
        '''

        l = self.listOfPackets + packets
        self.listOfPackets = sorted(l, key=itemgetter('time'))

        self.calculatePacketTimeDiff()
        self.findNumResent()
        self.calculateRTT()


    def merge(self, newPair):
        self.addPackets(newPair.listOfPackets)

    def get(key):
        if key == "rtt":
            return self.RTT
        elif key == "ptd":
            return self.packetTimeDiff
        elif key == "nr":
            return self.numResent
        elif key == "s":
            return self.server
        elif key == "c":
            return self.client
        else:
            return False
