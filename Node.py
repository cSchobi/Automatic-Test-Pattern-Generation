"""
Nodes that represent the input and output of the circuit
"""
class Node(object):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def connectInput(self, edge):
        pass
    
    def connectOutput(self, edge):
        pass

class InNode(Node):

    def __init__(self, name):
        super().__init__(name)
        self.outEdges = []

    def connectInput(self, edge):
        raise ValueError('InNode does not have an input')

    def connectOutput(self, edge):
        self.outEdges.append(edge)
        edge.connectInput(self)

class OutNode(Node):
    
    def __init__(self, name):
        super().__init__(name)

    def connectInput(self, edge):
        self.inEdge = edge
        edge.connectOutput(self)
    
    def connectOutPut(self, edge):
        raise ValueError('output of circuit cannot be connected to an input node')

"""
poss. 1:
    bend always at start of node: either change the incoming edge, delete preceding gate or add edge to inNode -> not possible because then certain input cannot be generated
poss. 2:
    bend before or after node: change all edges coming out of inNode and gateOutNode, change incoming edge of gateIn node and delete gate of output
poss. 2.5:
    change all edges coming out from InNode, delete gate and redirect input for gateOut and OutputNode, change incoming edge for gateinNode
poss 3:
    delete gate and redirect for endNode + GateOutNode, redirect outgoing edges for InNode and GateInNode
poss 4:
    redirect outgoing edges for all but Output; output -> delete gate
poss 5:
    add artificial gatenode of output gate: redirect outgoing edges for InNoe and GateOutNode, redirect Input for Output and GateInNode
"""