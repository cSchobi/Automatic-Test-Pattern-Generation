from Node import *

class Gate(object):
    
    def __init__(self, name):
        self.name = name
        self.inputs = []

    def __str__(self):
        return self.name

    def accept(self, visitor):
        print("abstract method for visitor")

    def setOutput(self, output):
        self.output = output

    def addInput(self, input):
        self.inputs.append(input)

    def setInputs(self, inputs):
        self.inputs = []
        for i in inputs:
            self.addInput(i)

class AndGate(Gate):
    def accept(self, visitor):
        visitor.visit_and(self)

class NandGate(Gate):
    def accept(self, visitor):
        visitor.visit_nand(self)

class OrGate(Gate):
    def accept(self, visitor):
        visitor.visit_or(self)

class NorGate(Gate):
    def accept(self, visitor):
        visitor.visit_nor(self)

class NotGate(Gate):
    def accept(self, visitor):
        visitor.visit_not(self)