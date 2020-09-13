# Automatic-Test-Pattern-Generation

This program was implemented as part of the course Hardware Design at Johannes Kepler University.

# Background
Integrated circuits need to be checked for production faults. There are several fault models that describe which faults can occur and what their consequences are. On such fault model is the Stuck-at fault. In this case a connection between gates does not transfer the electrical signal correctly and instead produces a constant LOW (0) or HIGH (1) signal. (For more details see for example: https://en.wikipedia.org/wiki/Stuck-at_fault). Since we cannot check all connections in a physical integrated circuit and can only simulate an input and observe the output of the circuit, we need a method that generates an input that allows us to ascertain whether the circuit has a Stuck-at fault by only observing the outputs. This program implements a SMT-solver based algorithm to generate inputs that alluws us to detect Stuck-at faults.

# Implementation

TODO
