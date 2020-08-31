from Circuit import Circuit

class ATPGCircuit(Circuit):
    """
    Representation of a circuit that can be used for generating input assignments
    to test for stuck at 1 or 0 faults. 
    """
    FAULT_SUFFIX = 'f'

    def __init__(self, faultfree: Circuit, faulty: Circuit):
        """
        The constructor takes two circuits that need to have the same input and output nodes. 
        These two circuits are merged into one and the output nodes are replaced with a miter structure.
        The input circuits must not be used afterwards.
        """
        self.inNodes = faultfree.inNodes
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

    def getFaultySignalName(self, signalName):
        """
        Return corresponding faulty signal name of the given signal.
        Assumes that generateMiter has been called before, otherwise this function is not useful
        """
        return signalName + ATPGCircuit.FAULT_SUFFIX