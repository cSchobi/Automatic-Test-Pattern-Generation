from Node import Node

class Edge(object):

    def connectOutput(self, node):
        self.outNode = node

    def connectInput(self, node):
        self.inNode = node

    def getOutput(self):
        return self.outNode

    def getInput(self):
        return self.inNode

    def __str__(self):
        return self.inNode.__str__() + " --> " + self.outNode.__str__()