import copy
import sys

from ATPG import *
from Circuit import Circuit
from Parser import Parser

def test(fileName, fault, signalName, inputIndex = None):
    c = Circuit()
    p = Parser(c, fileName)
    p.parse()
    atpg = ATPG(c, fault, signalName, inputIndex)
    atpg.solve()

def simple_test():
    print('simple test with 3 gates')
    test('simple_test.bench', Circuit.STUCK_AT_1_FAULT, 'e')
    # expect unsate

def c17_test1():
    print('test 1 of c17 bench')
    test('c17.bench', Circuit.STUCK_AT_1_FAULT, 'G11gat')

def c17_test2():
    print('test 2 of c17 bench')
    test('c17.bench', Circuit.STUCK_AT_0_FAULT, 'G22gat', 1)

def c432_test():
    print('test c432')
    test('c432.bench', Circuit.STUCK_AT_1_FAULT, 'G360gat')

def c1355_test():
    print('test c1355')
    test('c1355.bench', Circuit.STUCK_AT_0_FAULT, 'G996gat', 4)

def c7552_test():
    print('test c7552')
    test('c7552.bench', Circuit.STUCK_AT_1_FAULT, 'G940')

simple_test()
c17_test1()
c17_test2()
c432_test()
c1355_test()
c7552_test()