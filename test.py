import copy
import sys

from ATPG import *
from Circuit import Circuit
from Parser import Parser

DIRECTORY = "./bench_files"

def test(fileName, fault, signalName, inputIndex = None, useOutNode = None):
    c = Circuit()
    p = Parser(c, os.path.join(DIRECTORY, fileName))
    p.parse()
    atpg = ATPG(c)
    atpg.addFault(fault, signalName, inputIndex, useOutNode)
    atpg.solve()
    atpg.print()

def simple_test():
    print('simple test with 3 gates')
    test('simple_test.bench', Circuit.STUCK_AT_1_FAULT, 'f')
    # expect unsat

def c17_test1():
    print('test 1 of c17 bench')
    test('c17.bench', Circuit.STUCK_AT_1_FAULT, 'G11gat')

def c17_test2():
    print('test 2 of c17 bench')
    test('c17.bench', Circuit.STUCK_AT_0_FAULT, 'G22gat', inputIndex=1)

def c432_test():
    print('test c432')
    test('c432.bench', Circuit.STUCK_AT_1_FAULT, 'G360gat')

def c1355_test():
    print('test c1355')
    test('c1355.bench', Circuit.STUCK_AT_0_FAULT, 'G996gat', inputIndex=4)

def c7552_test():
    print('test c7552')
    test('c7552.bench', Circuit.STUCK_AT_1_FAULT, 'G550')

def c6288_test():
    print('test c6288')
    test('c6288.bench', Circuit.STUCK_AT_0_FAULT, 'G1371gat')

simple_test()
c17_test1()
c17_test2()
c432_test()
c1355_test()
c7552_test()
c6288_test()