from Node import *
from Edge import Edge
from Gate import *

"""
Represantion of a circuit object
"""
class Circuit(object):
    
    STUCK_AT_1_FAULT = InNode('TRUE')
    STUCK_AT_0_FAULT = InNode('FALSE')
    FAULT_SUFFIX = 'f'

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

    def addFault(self, fault, signalName, **kwargs):
        useOutNode = kwargs.get('useOutNode', None)
        if signalName in self.inNodes: # fault at input
            node = self.inNodes[signalName]
            # iterate over copy of list because deleting
            # while iterating gives undefined behaviour
            for e in node.outEdges[:]:
                node.disconnectOutput(e)
                e.connectInput(fault)

        # change Edge to the OutNode
        elif signalName in self.outNodes and useOutNode:
            node = self.outNodes[signalName]
            e = node.inEdge
            e.inNode.disconnectOutput(e)
            fault.connectOutput(e)

        # add fault around a gate
        elif signalName in self.gates:
            gate = self.gates[signalName]
            inputIndex = kwargs.get('inputIndex', None)
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


    def generateMiter(self, faulty):
        """
        Take another circuit _faulty_ that has the same input and output nodes as _self_
        and modify _self_ such that _self_ contains both circuits and connects their outputs
        via a miter structure. _self_ will have a new output which is the output of the
        miter structure
        """
        # 1. merge gates, edges and outNodes of faulty circuit into orignal circuit
        # copy gates
        for gate in faulty.gates.values():
            gate.name = self.getFaultySignalName(gate.name)
            self.gates[gate.name] = gate

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
            xor_gate = self.gates[xor_name]
            ctr += 1

            # reconnect the predecessor of OutNode to the XOR gate
            e = outNode.inEdge
            e.disconnectOutput()
            xor_gate.connectInput(e, 0)
 
            # do same for faulty circuit
            e = outNodeFaulty.inEdge # use edge to get predecessor instead of looking into gates/inNodes
            e.disconnectOutput()
            xor_gate.connectInput(e, 1)             

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

    def getFaultySignalName(self, signalName):
        """
        Return corresponding faulty signal name of the given signal.
        Assumes that generateMiter has been called before, otherwise this function is not useful
        """
        return signalName + Circuit.FAULT_SUFFIX

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