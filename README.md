# QOSF-Assessment-Task
Solution for QOSF Assessment Task 2021

Two versions of the incomplete solution have been implemented here. \
1. circuit_implementation.py is a partial solution using Grover's algorithm, implemented on a quantum circuit using Qiskit. 
2. grover.py implements Grover's algorithm on qubits in a quantum circuit, where the output is generated classically.

Method for the solution:

1.Create two quantum superposition states, one for the address bits, and one for the value bits in the input array
2.Since we know what the possible solution states are, create constraints (clauses in the dimacs file) for those states
3.Initialise the quantum circuit with an equal superposition with the states from an input array of any length and input values
4.Create a phase oracle using the built-in operator from the dimacs file
5.Using this oracle in the GroverOperator, implement Grover's algorithm on the composite state of address qubits and value qubits
6.Simulate the circuit
7.Get the counts for all the states, and check the location of the solution state present in the input array
8.Create a normalised quantum state of the index of the solution state in the input array and give it as output

Limitations:
Both the solutions allow the location of a single solution state in the input array, but fail if there are repeated solutions or more than one solution.\
circuit_implementation.py does not amplify the solution state if there are repeated values in the input array.\

The files are created and run in a folder called QOSF.\
The dimacs file for the phase oracle is created within the solution code.\


