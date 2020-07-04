from Node import *
from Edge import Edge
from Gate import *

class Circuit(object):
    
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

    def addOutNode(self, nodeName: str):
        assert(nodeName not in self.outNodes)
        self.outNodes[nodeName] = OutNode(nodeName)

    def getOutNode(self, nodeName: str):
        return self.outNodes[nodeName]

    def getOutNodeNames(self):
        return self.outNodes.keys()

    def containsOutNode(self, nodeName: str):
        return nodeName in self.outNodes

    def addEdge(self, inNode, outNode):
        self.edges.append(Edge(inNode, outNode))

    def addFault(self, signalName, fault, inputIndex = None):
        if signalName in self.inNodes: # fault at input
            node = self.inNodes[signalName]
            # iterate over copy of list because deleting
            # while iterating gives undefined behaviour
            for e in node.outEdges[:]:
                node.disconnectOutput(e)
                e.connectInput(fault)

        elif signalName in self.outNodes and inputIndex is None:
            node = self.outNodes[signalName]
            e = node.inEdge
            e.inNode.disconnectOutput(e)
            fault.connectOutput(e)

        elif signalName in self.gates:
            gate = self.gates[signalName]
            if inputIndex is None: # fault at output of gate
                node = gate.output
                # iterate over copy of list because deleting 
                # while iterating gives undefined behaviour
                for e in node.outEdges[:]: 
                    node.disconnectOutput(e)
                    fault.connectOutput(e)
            else: # fault at input
                node = gate.inputs[inputIndex]
                e = node.inEdge
                e.inNode.disconnectOutput(e)
                fault.connectOutput(e)                
        else:
            raise ValueError('cannot add fault because signal is not found')

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
    
    # helper function to connect output gates to output nodes
    # because connectGate only connects the inputs of the gate
    def connectOutput(self, outputNodeName: str):
        gate = self.gates[outputNodeName]
        outputNode = self.outNodes[outputNodeName]
        edge = Edge()
        self.edges.append(edge)
        gate.connectOutput(edge)
        outputNode.connectInput(edge)

    def generateMiter(self, faulty):
        # 1. merge gates, edges and outNodes of faulty circuit into orignal circuit
        # copy gates
        for gate in faulty.gates.values():
            gate.name = gate.name + "f"
            self.gates[gate.name] = gate
        # copy outNodes
        """for node in faulty.outNodes.values():
            node.name = node.name + "f"
            self.outNodes[node.name] = node"""
        # copy edges
        for e in faulty.edges:
            self.edges.append(e)
        # redirect edges from input in faulty to input of original circuit
        for inNode in faulty.inNodes.values():
            for e in inNode.outEdges[:]:
                inNode.disconnectOutput(e)
                # connect edge to inNode of original circuit with same name
                e.connectInput(self.inNodes[inNode.name]) 

        # 2. add miter structure; replace outNodes with XOR gates, add final Or gate and add 1 outNode
        ctr = 0
        xor_gates = []
        for (outName, outNode) in self.outNodes.items():
            outNodeFaulty = faulty.getOutNode(outName)
            xor_name = "miter_XOR_%d" % ctr
            self.addGate(xor_name, 'xor', 2)
            xor_gates.append(self.gates[xor_name])
            ctr += 1
            outGate = self.gates[outName]
            e = outNode.inEdge
            outGate.disconnectOutput(e)
            self.edges.remove(e)
            self.connectGate(outName, xor_name, 0)

            outGate = faulty.gates[outName]
            e = outNodeFaulty.inEdge
            outGate.disconnectOutput(e)
            self.edges.remove(e)
            self.connectGate(outName + "f", xor_name, 1)
        pass
        self.outNodes = {}
        # generate final OR and connect XORs to it
        miter_or_name = "miter_OR"
        self.addGate(miter_or_name, 'or', ctr)
        assert(len(xor_gates) == ctr)
        for (ctr, gate) in enumerate(xor_gates):
            self.connectGate(gate.name, miter_or_name, ctr)
        
        self.addOutNode(miter_or_name)
        self.connectOutput(miter_or_name)

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