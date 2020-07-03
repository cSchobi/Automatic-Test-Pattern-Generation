import re
from Node import *
from Circuit import *
from Gate import *

class Parser(object):

    # regular expression to match lines
    INPUT_PATTERN = re.compile("INPUT\((.*)\)")
    OUTPUT_PATTERN = re.compile("OUTPUT\((.*)\)")
    GATE_PATTERN = re.compile('(.*) = (.*)\((.*)\)')


    def __init__(self, circuit: Circuit, fileName):
        self.circuit = circuit
        self.fileName = fileName

    def parse(self):
        f = open(self.fileName, 'r')
        for line in f:
            if line.startswith('#') or not line or line == "\n":
                continue
            m = Parser.INPUT_PATTERN.match(line)
            if m:
                node = InNode(m.group(1))
                self.circuit.addInNode(node)
                continue
            m = Parser.OUTPUT_PATTERN.match(line)
            if m:
                node = OutNode(m.group(1))
                self.circuit.addOutNode(node)
                continue
            self.parseGate(line)

        pass

    def parseGate(self, line):
        (gate, gateInNodeNames) = self.getGate(line)
        gateName = gate.name
        self.circuit.addGate(gate)
        if self.circuit.containsOutNode(gateName):
            gateOutNode = self.circuit.getOutNode(gateName)
        else:
            gateOutNode = GateOutNode(gateName)
            self.circuit.addNode(gateOutNode)
        gateInNodes = [GateInNode(gateName + " in %d" % ctr) for ctr, nodeName in enumerate(gateInNodeNames)]
        gate.setOutput(gateOutNode)
        gate.setInputs(gateInNodes)

        # add edges
        for gateInNode in gateInNodes:
            self.circuit.addNode(gateInNode)
        outNodes = [self.circuit.getNode(nodeName) for nodeName in gateInNodeNames]
        for (inNode, outNode) in zip(outNodes, gateInNodes):
            self.circuit.addEdge(inNode, outNode)

    def getGate(self, line):
        m = Parser.GATE_PATTERN.match(line)
        if m is None:
            print("error")
            print("line:", line)
            print("after line")
        gateName = m.group(1)
        gateType = m.group(2)
        gateInputs = m.group(3).split(', ')
        if gateType == 'and':
            gate = AndGate(gateName)
        elif gateType == 'nand':
            gate = NandGate(gateName)
        elif gateType == 'or':
            gate = OrGate(gateName)
        elif gateType == 'nor':
            gate = NorGate(gateName)
        elif gateType == 'not':
            gate = NotGate(gateName)
        else:
            print("unexpected gate type")

        return (gate, gateInputs)