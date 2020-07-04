from Node import *
from Edge import *

class Gate(object):
    def __init__(self, name, inputSize):
        self.name = name
        self.output = OutputNode(self)
        self.inputs = [InputNode(self) for i in range(inputSize)]

    def __str__(self):
        return self.name

    def connectOutput(self, edge: Edge):
        self.output.connect(edge)
        edge.connectInput(self.output)

    def connectInput(self, edge: Edge, i):
        self.inputs[i].connect(edge)
        edge.connectOutput(self.inputs[i])

    def getInputNodeIndex(self, node):
        return self.inputs.index(node)

    def accept(self, visitor):
        print("abstract method for visitor")    


class AndGate(Gate):
    def accept(self, visitor):
        visitor.visit_and(self)

    def __str__(self):
        return 'and_' + super().__str__()

class NandGate(Gate):
    def accept(self, visitor):
        visitor.visit_nand(self)

    def __str__(self):
        return 'nand_' + super().__str__()

class OrGate(Gate):
    def accept(self, visitor):
        visitor.visit_or(self)

    def __str__(self):
        return 'or_' + super().__str__()

class NorGate(Gate):
    def accept(self, visitor):
        visitor.visit_nor(self)

    def __str__(self):
        return 'nor_' + super().__str__()

class NotGate(Gate):
    def accept(self, visitor):
        visitor.visit_not(self)

    def __str__(self):
        return 'not_' + super().__str__()     

class XorGate(Gate):
    def accept(self, visitor):
        visitor.visit_xor(self)

    def __str__(self):
        return 'xor_' + super().__str__()   

class OutputNode(object):
    def __init__(self, gate):
        self.outEdges = []
        self.gate = gate

    def connect(self, edge):
        self.outEdges.append(edge)

    def disconnectOutput(self, edge):
        self.outEdges.remove(edge)
        edge.disconnectInput()
        
    def __str__(self):
        return self.gate.__str__()

class InputNode(object):
    def __init__(self, gate):
        self.inEdge = None
        self.gate = gate

    def connect(self, edge):
        self.inEdge = edge

    def __str__(self):
        return self.gate.__str__() + '_'+ self.gate.getInputNodeIndex(self).__str__()