from Node import *
from Edge import Edge
class Circuit(object):
    
    def __init__(self):
        self.inNodes = {}
        self.outNodes = {}
        self.gates = {}
        self.interiorNodes = {}
        self.edges = []

    def addNode(self, node):
        if isinstance(node, InteriorNode):
            self.addInteriorNode(node)
        elif isinstance(node, InNode):
            self.addInNode(node)
        elif isinstance(node, OutNode):
            self.addOutNode(node)
        else:
            raise ValueError('unexpected node type')

    def addInNode(self, node):
        assert(node.name not in self.inNodes)
        self.inNodes[node.name] = node

    def getInNode(self, nodeName):
        return self.inNodes[nodeName]

    def addOutNode(self, node):
        assert(node.name not in self.outNodes)
        self.outNodes[node.name] = node

    def getOutNode(self, nodeName):
        return self.outNodes[nodeName]

    def addInteriorNode(self, node):
        assert(node.name not in self.interiorNodes)
        self.interiorNodes[node.name] = node

    def getInteriorNode(self, nodeName):
        return self.interiorNodes[nodeName]

    def addGate(self, gate):
        assert(gate.name not in self.gates)
        self.gates[gate.name] = gate

    def addEdge(self, inNode, outNode):
        self.edges.append(Edge(inNode, outNode))

    def addFault(self, faultPos):
        pass

    def containsOutNode(self, nodeName):
        return nodeName in self.outNodes

    def getNode(self, nodeName):
        if nodeName in self.inNodes:
            return self.getInNode(nodeName)
        elif nodeName in self.interiorNodes:
            return self.getInteriorNode(nodeName)
        elif nodeName in self.outNodes:
            return self.getOutNode(nodeName)
        else:
            raise ValueError('node ' + nodeName + ' is no in the circuit')

    def print(self):
        print("input")   
        for node in self.inNodes.values():
            print(node)
        print("output")
        for node in self.outNodes.values():
            print(node)
        print("gates")
        for gate in self.gates.values():
            print(gate)
        print("edges")
        for e in self.edges:
            print(e)
        print("interior nodes")
        for i in self.interiorNodes:
            print(i)