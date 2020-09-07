from Circuit import *
from Node import *

class ATPGCircuit(Circuit):
    """
    Representation of a circuit that can be used for generating input assignments
    to test for stuck at 1 or 0 faults. 
    """
    FAULT_SUFFIX = '_f'

    def __init__(self, faultfree: Circuit, faulty: Circuit):
        """
        The constructor takes two circuits that need to have the same input and output nodes. 
        These two circuits are merged into one and the output nodes are replaced with a miter structure.
        The input circuits must not be used afterwards.
        """
        self.inNodes = faultfree.inNodes
        self.faultyInNodes = {}
        self.outNodes = faultfree.outNodes
        self.gates = faultfree.gates
        self.edges = faultfree.edges
        self.generateMiter(faulty)        

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

        # copy inNodes
        for inNode in faulty.inNodes.values():
            inNode.name = self.getFaultySignalName(inNode.name)
            self.faultyInNodes[inNode.name] = inNode


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

    def getFaultySignalName(self, signalName):
        """
        Return corresponding faulty signal name of the given signal.
        Assumes that generateMiter has been called before, otherwise this function is not useful
        """
        return signalName + ATPGCircuit.FAULT_SUFFIX

    def addFault(self, fault, signalName, **kwargs):
        """ variables are set to store where the fault is """
        self.fault = fault
        self.signalName = signalName
        self.useOutNode = kwargs.get('useOutNode', None)
        self.inputIndex = kwargs.get('inputIndex', None)
        faultySignalName = self.getFaultySignalName(signalName)
        if signalName in self.inNodes: # fault at input
            node = self.faultyInNodes[faultySignalName]
            # iterate over copy of list because deleting
            # while iterating gives undefined behaviour
            for e in node.outEdges[:]:
                node.disconnectOutput(e)
                fault.connectOutput(e)

        # change Edge to the OutNode
            """"elif signalName in self.outNodes and useOutNode:
            node = self.outNodes[signalName]
            e = node.inEdge
            e.inNode.disconnectOutput(e)
            fault.connectOutput(e) """

        # add fault around a gate
        elif faultySignalName in self.gates:
            gate = self.gates[faultySignalName]
            if self.inputIndex is None: # fault at output of gate
                node = gate.output
                # iterate over copy of list because deleting 
                # while iterating gives undefined behaviour
                for e in node.outEdges[:]: 
                    node.disconnectOutput(e)
                    fault.connectOutput(e)
            else: # fault at input
                node = gate.inputs[self.inputIndex]
                e = node.inEdge
                e.inNode.disconnectOutput(e)
                fault.connectOutput(e)                
        else:
            raise ValueError('cannot add fault because signal is not found')   

    def removeFault(self):
        faultySignalName = self.getFaultySignalName(self.signalName)
        if self.signalName in self.inNodes: # fault at input
            faultyInNode = self.faultyInNodes[faultySignalName]
            for e in self.fault.outEdges[:]: # BUG
                self.fault.disconnectOutput(e)
                faultyInNode.connectOutput(e)

        elif self.signalName in self.gates:
            gate = self.gates[faultySignalName]
            if self.inputIndex is None:
                node = gate.output
                for e in self.fault.outEdges[:]:
                    self.fault.disconnectOutput(e)
                    node.connectOutput(e)
            else:
                # get corresponding gate and input node from fault free circuit
                faultFreeGate = self.gates[self.signalName] # corresponding gate in fault free circuit
                faultFreeNode = faultFreeGate.inputs[self.inputIndex]
                node = faultFreeNode.inEdge.inNode
                if isinstance(node, OutputNode):
                    nodeInFaultyCircuit = self.gates[self.getFaultySignalName(node.gate.name)]
                elif isinstance(node, InNode):
                    nodeInFaultyCircuit = self.faultyInNodes[self.getFaultySignalName(node.name)]
                else:
                    print(type(faultFreeNode))
                    raise ValueError('Edge is connected to invalid node')
                
                assert(len(self.fault.outEdges) == 1)
                e = self.fault.outEdges[0]
                self.fault.disconnectOutput(e)
                nodeInFaultyCircuit.connectOutput(e) # BUG get corresponding node in faultfree cricuit and reroute edge

        self.signalName = None
        self.fault = None
        self.inputIndex = None
        self.useOutNode = None

