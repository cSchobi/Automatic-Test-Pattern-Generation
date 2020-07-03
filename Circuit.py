from Node import *
from Edge import Edge
from Gate import *

class Circuit(object):
    
    def __init__(self):
        self.inNodes = {}
        self.outNodes = {}
        self.gates = {}
        self.edges = []

    def addNode(self, node):
        if isinstance(node, InNode):
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

    def getOutNodes(self):
        return self.outNodes.values()

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
        elif nodeName in self.outNodes:
            return self.getOutNode(nodeName)
        else:
            raise ValueError('node ' + nodeName + ' is no in the circuit')

    def addGate(self, gateName, gateType, numInputs):
        if gateType == 'and':
            gate = AndGate(gateName, numInputs)
        elif gateType == 'nand':
            gate = NandGate(gateName, numInputs)
        elif gateType == 'or':
            gate = OrGate(gateName, numInputs)
        elif gateType == 'nor':
            gate = NorGate(gateName, numInputs)
        elif gateType == 'not':
            gate = NotGate(gateName, numInputs)
        elif gateType == 'xor':
            gate = XorGate(gateName, numInputs)
        else:
            raise ValueError('unexpected gate type')
        self.gates[gate.name] = gate

    def connectGate(self, signalName, gateName, ctr):
        if signalName in self.gates:
            node = self.gates[signalName]
        elif signalName in self.inNodes:
            node = self.inNodes[signalName]
        else:
            raise ValueError('cannot connect edge to illegal source')
        
        edge = Edge()
        self.edges.append(edge)
        node.connectOutput(edge)
        self.gates[gateName].connectInput(edge, ctr)
    
    def connectOutput(self, outputNode):
        gate = self.gates[outputNode.name]
        edge = Edge()
        self.edges.append(edge)
        gate.connectOutput(edge)
        outputNode.connectInput(edge)

    def addFault(self, nodeName):
        pass

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