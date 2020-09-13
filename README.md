# Automatic-Test-Pattern-Generation

This program was implemented as part of the course Hardware Design at Johannes Kepler University.

# Background
Integrated circuits need to be checked for production faults. There are several fault models that describe which faults can occur and what their consequences are. On such fault model is the Stuck-at fault. In this case a connection between gates does not transfer the electrical signal correctly and instead produces a constant LOW (0) or HIGH (1) signal. (For more details see for example: https://en.wikipedia.org/wiki/Stuck-at_fault). Since we cannot check all connections in a physical integrated circuit and can only simulate an input and observe the output of the circuit, we need a method that generates an input that allows us to ascertain whether the circuit has a Stuck-at fault by only observing the outputs. This program implements a SMT-solver based algorithm to generate inputs that alluws us to detect Stuck-at faults.

# Algorithm

TODO 

# Implementation
The input files that describe the circuit need to have the Bench format (for examples see: https://ddd.fit.cvut.cz/prj/Benchmarks/).
![Internal datastructure of parsed circuit](images/input_circuit.png)
The input file is parsed and an internal data structure is built up. This data structure has Gates, Nodes and Edges that represent the circuit. 

Next a copy of the circuit is made and is connected to the original circuit by connecting the corresponding input nodes and appending a miter structure to the outputs. 
![Circuit that contains original circuit, the copy and the miter structure](images/ATPCircuit.png)

Then the user can choose the location of the fault and whether it is a Stuck-at-0 or Stuck-at-1 fault. The circuit with the miter structure is changed accordingly. The image below shows an example where the output of the Nand Gate  g11 is stuck at 1.
![Circuit that contains original circuit, the copy and the miter structure](images/ATPGCircuit_with_fault.png)

This circuit is then encoded as an SMT instance and passed to the SMT solver Z3. If the given fault can be detected, an input pattern that allows us to check for the given fault can be extracted.
