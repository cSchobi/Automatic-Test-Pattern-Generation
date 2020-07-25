from Node import Node

class Edge(object):
    """
    Represents a single edge connecting two nodes
    """

    def connectOutput(self, node):
        self.outNode = node

    def connectInput(self, node):
        self.inNode = node

    def disconnectOutput(self):
        self.outNode = None

    def disconnectInput(self):
        self.inNode = None

    def getOutput(self):
        return self.outNode

    def getInput(self):
        return self.inNode

    def __str__(self):
        return self.inNode.__str__() + " --> " + self.outNode.__str__()