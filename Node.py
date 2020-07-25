class Node(object):
    """
    Abstract class that represent connection nodes
    """
    
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def connectInput(self, edge):
        pass
    
    def connectOutput(self, edge):
        pass

class InNode(Node):
    """
    Represents an input of the circuit
    """

    def __init__(self, name):
        super().__init__(name)
        self.outEdges = []

    def connectInput(self, edge):
        raise ValueError('InNode does not have an input')

    def connectOutput(self, edge):
        self.outEdges.append(edge)
        edge.connectInput(self)

    def disconnectOutput(self, edge):
        self.outEdges.remove(edge)
        edge.disconnectInput()

class OutNode(Node):
    """
    Represents an output of a circuit
    """
    
    def __init__(self, name):
        super().__init__(name)

    def connectInput(self, edge):
        self.inEdge = edge
        edge.connectOutput(self)
    
    def disconnectInput(self):
        self.inEdge.disconnectOutput()
        self.inEdge = None
        
    def connectOutPut(self, edge):
        raise ValueError('output of circuit cannot be connected to an input node')