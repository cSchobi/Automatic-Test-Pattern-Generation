from z3 import *

from Gate import *


class GateConstraintVisitor(object):
    def __init__(self, s, vars):
        self.s = s
        self.vars = vars

    def getVars(self, gate):
        return (
            self.vars[gate.output.__str__()],
            [self.vars[node.__str__()] for node in gate.inputs])

    def setConstraint(self, gate: Gate, constraintFun):
        (outputVar, inputVars) = self.getVars(gate)
        constraint = constraintFun(inputVars)
        self.s.add(outputVar == constraint)

    def visit_and(self, gate: AndGate):
        self.setConstraint(gate, lambda x: And(x))

    def visit_nand(self, gate: NandGate):
        self.setConstraint(gate, lambda x: Not(And(x)))

    def visit_or(self, gate: OrGate):
        self.setConstraint(gate, lambda x: Or(x))

    def visit_nor(self, gate: NorGate):
        self.setConstraint(gate, lambda x: Not(Or(x)))

    def visit_not(self, gate: NotGate):
        self.setConstraint(gate, lambda x: Not(x[0]))

    def visit_xor(self, gate: XorGate):
        self.setConstraint(gate, lambda x: Xor(x[0], x[1]))

    def visit_buf(self, gate: BufGate):
        self.setConstraint(gate, lambda x: x[0])