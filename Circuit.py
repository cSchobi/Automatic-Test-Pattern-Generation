from Node import *
from Edge import Edge
from Gate import *


class Circuit(object):
    """
    Representation of a circuit object
    """
    
    STUCK_AT_1_FAULT = InNode('TRUE')
    STUCK_AT_0_FAULT = InNode('FALSE')

    def __init__(self):
        self.inNodes = {}
        self.outNodes = {}
        self.gates = {}
        self.edges = []

    def addInNode(self, nodeName: str):
        assert(nodeName not in self.inNodes)
        self.inNodes[nodeName] = InNode(nodeName)

    def getInNode(self, nodeName: str):
        return self.inNodes[nodeName]

    def getInNodes(self):
        return self.inNodes.values()

    def getInNodeNames(self):
        return self.inNodes.keys()

    def getGateNames(self):
        return self.gates.keys()

    def getGates(self):
        return self.gates.values()

    def addOutNode(self, nodeName: str):
        assert(nodeName not in self.outNodes)
        self.outNodes[nodeName] = OutNode(nodeName)

    def getOutNode(self, nodeName: str):
        return self.outNodes[nodeName]

    def getOutNodes(self):
        return self.outNodes.values()

    def getOutNodeNames(self):
        return self.outNodes.keys()

    def containsOutNode(self, nodeName: str):
        return nodeName in self.outNodes

    def addEdge(self, inNode, outNode):
        self.edges.append(Edge(inNode, outNode))

    def addGate(self, gateName, gateType, numInputs):
        gateType = gateType.lower()
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
        elif gateType == 'buf':
            gate = BufGate(gateName, numInputs)
        else:
            print(gateName, gateType, numInputs)
            raise ValueError('unexpected gate type')
        self.gates[gate.name] = gate

    # connect a signal to a specified input of a gate
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
    
    # helper function to connect output gates (or inputNodes) to output nodes
    def connectOutput(self, outputNodeName: str):
        if outputNodeName in self.gates:
            signal = self.gates[outputNodeName]
        elif outputNodeName in self.inNodes:
            signal = self.inNodes[outputNodeName]
        else:
            raise ValueError('cannot connect output')
        outputNode = self.outNodes[outputNodeName]
        edge = Edge()
        self.edges.append(edge)
        signal.connectOutput(edge)
        outputNode.connectInput(edge)

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

    def __deepcopy__(self, memo):
        cpy = self.__class__()
        for nodeName, node in self.inNodes.items():
            cpy.addInNode(nodeName)

        for nodeName, node in self.outNodes.items():
            cpy.addOutNode(nodeName)

        for gateName, gate in self.gates.items():
            gateCpy = gate.__class__(gateName, len(gate.inputs))
            cpy.gates[gateName] = gateCpy

            #connect gateinputs
            for ctr, inputNode in enumerate(gate.inputs):
                node = inputNode.inEdge.getInput()
                if isinstance(node, OutputNode):
                    signalName = node.gate.name
                else:
                    signalName = node.name
                cpy.connectGate(signalName, gateName, ctr)

        for nodeName in self.getOutNodeNames():
            cpy.connectOutput(nodeName)
        return cpy