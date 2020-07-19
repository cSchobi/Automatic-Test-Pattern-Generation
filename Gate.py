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
        self.output.connectOutput(edge)
        edge.connectInput(self.output)

    def disconnectOutput(self, edge: Edge):
        self.output.disconnectOutput(edge)

    def connectInput(self, edge: Edge, i):
        self.inputs[i].connectInput(edge)
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

class BufGate(Gate):
    def accept(self, visitor):
        visitor.visit_buf(self)

    def  __str__(self):
        return 'buf_' + super().__str__()

class OutputNode(Node):
    def __init__(self, gate):
        self.outEdges = []
        self.gate = gate

    def connectOutput(self, edge):
        self.outEdges.append(edge)

    def connectInput(self, edge):
        raise ValueError('output node of gate has no input')

    def disconnectOutput(self, edge):
        self.outEdges.remove(edge)
        edge.disconnectInput()
        
    def __str__(self):
        return self.gate.__str__()

class InputNode(Node):
    def __init__(self, gate):
        self.inEdge = None
        self.gate = gate

    def connectInput(self, edge):
        self.inEdge = edge

    def disconnectInput(self):
        self.inEdge = None

    def connectOutput(self, edge):
        raise ValueError('inputNode of gate has no output')

    def __str__(self):
        return self.gate.__str__() + '_'+ self.gate.getInputNodeIndex(self).__str__()