from ServerClientTuple import ServerClientTuple

#write code for clustering (or labeling / categorizing) data
#(for example, see if you use some features to group the data, and see how well
#do those groups align with location information)

def group_by(key, data):
    '''
    key can be:
    rtt: round trip time
    ptd: the averge time between two packets
    nr: number of resent packets
    s: server IP
    c: client IP

    Data is a list of ServerClientTuple's
    '''
    groups = {}
    for d in data:
        if d.get(key) == False:
            print "data does not have key: %s" % key
            return false
        if groups.has_key(d.get(key)):
            d[key].append([d])
        else:
            d[key] = [d]

    return groups
