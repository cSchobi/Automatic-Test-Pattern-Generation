from Circuit import Circuit
from Parser import Parser
import sys

c = Circuit()
p = Parser(c, 'c17.bench')
p.parse()
c.print()

c.addFault('G11gat', Circuit.TRUE_NODE)
c.print()