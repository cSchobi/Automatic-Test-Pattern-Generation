from Circuit import Circuit
from Parser import Parser
import sys

c = Circuit()
p = Parser(c, 'c432.bench')
p.parse()
c.print()