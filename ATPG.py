from z3 import *
from Circuit import *
from ATPGCircuit import *
from GateConstraintVisitor import *
"""
Class that generates an input for a given fault and circuit, 
using the SMT solver z3
"""

class ATPG(object):
    def __init__(self, circuit: Circuit, fault, signalName, inputIndex = None, useOutNode = None):
        self.s = Solver()
        self.vars = {} # Map with all variables of SMT solves 

        faulty = copy.deepcopy(circuit)
        faulty.addFault(fault, signalName, inputIndex=inputIndex, useOutNode=useOutNode)
        self.circuit = ATPGCircuit(circuit, faulty)
        self.declareVars()
        self.setGateConstraints()
        self.setEdgeConstraints()
        self.setOutputConstraint()

    def declareVars(self):
        for gate in self.circuit.getGates():
            var_name = gate.output.__str__()
            self.vars[var_name] = Bool(var_name)
            for inputNode in gate.inputs:
                var_name = inputNode.__str__()
                self.vars[var_name] = Bool(var_name)
        for inNode in self.circuit.getInNodes():
            var_name = inNode.__str__()
            self.vars[var_name] = Bool(var_name)
        for outNode in self.circuit.getOutNodes():
            var_name = outNode.__str__()
            self.vars[var_name] = Bool(var_name)

        self.vars[Circuit.STUCK_AT_1_FAULT.__str__()] = Bool(
            Circuit.STUCK_AT_1_FAULT.__str__())
        self.s.add(self.vars[Circuit.STUCK_AT_1_FAULT.__str__()] == True)
        self.vars[Circuit.STUCK_AT_0_FAULT.__str__()] = Bool(
            Circuit.STUCK_AT_0_FAULT.__str__())
        self.s.add(self.vars[Circuit.STUCK_AT_0_FAULT.__str__()] == False)

    def setEdgeConstraints(self):
        for e in self.circuit.edges:
            inNode = e.inNode
            outNode = e.outNode
            self.s.add(self.vars[inNode.__str__()] ==
                       self.vars[outNode.__str__()])

    def setGateConstraints(self):
        visitor = GateConstraintVisitor(self.s, self.vars)
        for gate in self.circuit.getGates():
            gate.accept(visitor)

    def setOutputConstraint(self):
        assert(len(self.circuit.getOutNodeNames()) == 1)
        outNodeName = list(self.circuit.getOutNodeNames())[0]
        outNode = self.circuit.getOutNode(outNodeName)
        self.s.add(True == self.vars[outNode.__str__()])

    def solve(self):
        print("solver status")
        if self.s.check() == sat:
            self.print()
        else:
            print("unsat")
            
    def print(self):
        print("input vars:")
        if self.s.check() == sat:
            m = self.s.model()
            for inNodeName in self.circuit.getInNodeNames():
                var = self.vars[inNodeName]
                print(inNodeName, m[var])

            print("gate values: original | faulty")
            for gateName in self.circuit.gates:
                faultyGatename = self.circuit.getFaultySignalName(gateName)
                if faultyGatename in self.circuit.gates: # filter faulty gates
                    gate = self.circuit.gates[gateName]
                    var = self.vars[gate.output.__str__()]
                    faultyGate = self.circuit.gates[faultyGatename]
                    varFaulty = self.vars[faultyGate.output.__str__()]

                    print('{0}: {1!s:<5s} | {2!s:<5s}'.format(gateName, m[var], m[varFaulty]))

                    for (i, (inputNode, faultyInputNode)) in enumerate(zip(gate.inputs, faultyGate.inputs)):
                        var = self.vars[inputNode.__str__()]
                        varFaulty = self.vars[faultyInputNode.__str__()]
                        print('\t{0}: {1!s:<5s} | {2!s:<5s}'.format(i, m[var], m[varFaulty]))