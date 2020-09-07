import os
from Circuit import *
from Parser import *
from ATPG import *
import copy
import logging
import time

DIRECTORY = "../bench_files"

def run_test(atpg : ATPG, fault, signalName, inputIndex = None, useOutNode = None):

        atpg.addFault(fault, signalName, inputIndex, useOutNode)
        atpg.solve()
        log_info = signalName +\
                                ("[" + str(inputIndex) + "]" if inputIndex is not None else "") + \
                                ("[Output]" if useOutNode is not None else "") + \
                               ": "
        if atpg.s.check() == sat:
            inValues =[atpg.s.model()[atpg.vars[nodeName]] for nodeName in atpg.circuit.getInNodeNames()]
            inValuesStr = "".join([("1" if is_true(i) else "0") for i in inValues])
            logging.info(log_info + inValuesStr)
        else:
            logging.info(log_info + "No test case possible")
        atpg.removeFault()

logging.basicConfig(format = '%(message)s', filename='benchmark_results.log', filemode='w', level=logging.INFO)

for filename in os.listdir(DIRECTORY):
    logging.info("START with " + filename)
    c = Circuit()
    p = Parser(c, os.path.join(DIRECTORY, filename))
    p.parse()
    atpg = ATPG(c)
    logging.info("Inputs: " + " ".join(c.getInNodeNames()))
    start = time.process_time()
    for fault in [Circuit.STUCK_AT_0_FAULT, Circuit.STUCK_AT_1_FAULT]:
        logging.info("START with stuck at " + ("1" if fault == Circuit.STUCK_AT_1_FAULT else "0") + " fault")
        for inputNodeName in c.inNodes:
            run_test(atpg, fault, inputNodeName)

        for gateName in c.gates:
            # output of gate
            run_test(atpg, fault, gateName)
            for i in range(len(c.gates[gateName].inputs)):
                # inputs of gate
                run_test(atpg, fault, gateName, inputIndex = i)

        """ for outNodeName in c.outNodes:
            run_test(atpg, fault, outNodeName, useOutNode = True) """
        logging.info("FINISHED with stuck at " + ("1" if fault is Circuit.STUCK_AT_1_FAULT else "0") + " fault")
    end = time.process_time()
    logging.info(filename + " ELAPSED TIME: " + str(end - start) + " seconds")
    print(filename + " ELAPSED TIME: " + str(end - start) + " seconds")
    logging.info("FINISHED with " + filename)