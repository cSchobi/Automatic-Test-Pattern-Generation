from Node import Node

class Edge(object):

    def __init__(self, inNode, outNode):
        self.inNode = inNode
        self.outNode = outNode

    def __str__(self):
        return self.inNode.__str__() + " --> " + self.outNode.__str__()
