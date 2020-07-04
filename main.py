from Circuit import Circuit
from Parser import Parser
import sys
import copy

c = Circuit()
p = Parser(c, 'c17.bench')
p.parse()
c.print()

faulty = copy.deepcopy(c)
faulty.addFault('G11gat', Circuit.STUCK_AT_1_FAULT)
c.print()
c.generateMiter(faulty)
c.print()