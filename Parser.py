import re
from Node import *
from Circuit import *
from Gate import *

class Parser(object):
    """
    Parser for parsing bench files into an internal data structure
    """

    # regular expression to match lines
    INPUT_PATTERN = re.compile("INPUT\((.*)\)")
    OUTPUT_PATTERN = re.compile("OUTPUT\((.*)\)")
    GATE_PATTERN = re.compile('(.*) = (.*)\((.*)\)')

    def __init__(self, circuit: Circuit, fileName: str):
        self.circuit = circuit
        self.fileName = fileName

    def parse(self):
        f = open(self.fileName, 'r')
        for line in f:
            if line.startswith('#') or not line or line == "\n":
                continue
            m = Parser.INPUT_PATTERN.match(line)
            if m:
                self.circuit.addInNode(m.group(1))
                continue
            m = Parser.OUTPUT_PATTERN.match(line)
            if m:
                self.circuit.addOutNode(m.group(1))
                continue
            self.parseGate(line)

        # connect output nodes to gates
        for nodeName in self.circuit.getOutNodeNames():
            self.circuit.connectOutput(nodeName)

    def parseGate(self, line):
        (gateName, gateType, signalNames) = self.getGate(line)
        self.circuit.addGate(gateName, gateType, len(signalNames))
        
        # add edges
        for ctr, signalName in enumerate(signalNames):
            self.circuit.connectGate(signalName, gateName, ctr)

    def getGate(self, line):
        m = Parser.GATE_PATTERN.match(line)
        if m is None:
            raise ValueError('invalid gate line: ', line)
        gateName = m.group(1)
        gateType = m.group(2)
        gateInputs = m.group(3).split(', ')

        return (gateName, gateType, gateInputs)