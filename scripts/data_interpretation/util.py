import math, random

class Point:
    def __init__(self, x=None, y=None):
        if x is None or y is None:
            self.x = random.uniform(-50,50)
            self.y = random.uniform(-50,50)
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def mult_const(self, c):
        return Point(self.x*c, self.y*c)

    def mag(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def unit(self):
        if self.mag() == 0:
            return Point(0,0)
        else:
            return Point(self.x/self.mag(), self.y/self.mag())

    def __str__(self):
        return "(%.2f), (%.2f)" % (self.x, self.y)



def dist(a, b):
    return math.sqrt(math.pow((b.x - a.x), 2) + math.pow((b.y - a.y), 2))


def error(RTT, a, b):
    return math.pow(RTT - dist(a,b), 2)


def total_error(latency_mat, coords):
    nodes = len(coords)
    total_error = 0
    for i in xrange(0,nodes):
        n1 = coords[i]
        for j in xrange(0,nodes):
            n2 = coords[j]
            total_error += error(latency_mat[i][j], n1, n2)

    return total_error


if __name__ == "__main__":
    p = Point(0,1)
    pp = Point(2,3)
    print p, pp
