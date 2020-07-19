import copy
import sys

from ATPG import *
from Circuit import Circuit
from Parser import Parser

c = Circuit()
p = Parser(c, 'c17.bench')
p.parse()

atpg = ATPG(c, Circuit.STUCK_AT_1_FAULT, 'G11gat')
atpg.solve()
