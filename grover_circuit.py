import matplotlib.pyplot as plt
import numpy as np
import math
# importing Qiskit
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram
from qiskit.utils import QuantumInstance
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import PhaseOracle, GroverOperator
from qiskit.quantum_info import DensityMatrix, Operator, Statevector
# import basic plot tools
import os
from functions_qosf import solution_states, init_vector

array_i = [1, 5, 7, 10] #input array; accept input, or create a random array - consult qosf doc
print(array_i)
L=len(array_i)		#length of input array
highest = max(array_i)	
#print(highest)
#l = math.ceil(math.log(highest,2))
l_b = bin(highest)[2:]
l = len(l_b)
print(l)
bL_b = bin(len(array_i)-1)[2:]
bL = len(bL_b)	
#print(bL)
N = 2**l
M = 2**(l+bL)
#----------------create circuit-----------------------------------------

#address_bits = QuantumRegister(bL, name='a')
value_bits = QuantumRegister(l+bL, name='v')
#phase_bit = QuantumRegister(1, name='p')
grover_circuit = QuantumCircuit(value_bits)


#-------------------initialise qubits-----------------------------------

def init_vector(array_i, M):				#initialisation vector
	norm = 0
	init_vec = [0]*M
	for i in range(len(array_i)):
		index_bits = bin(i)[2:].zfill(bL)
		data_bits = bin(array_i[i])[2:].zfill(l)
		index = int((index_bits+data_bits),2)
		init_vec[index] = 1
	for i in init_vec:
		norm = norm + i
	for i in range(len(init_vec)):
		init_vec[i] = init_vec[i]/np.sqrt(norm)
	return init_vec
init_vec = init_vector(array_i, M)			
#print(init_vec)

grover_circuit.initialize(init_vec,  value_bits)	#initialise value bits



#--------------------create solution states from function--------------------------

solution_states = solution_states(l)		#solution states (2 bitstrings of alternating bits) for the length l


#----------------------create phase oracle----------------------------------------
q = QuantumRegister(l,'q')
qc = QuantumCircuit(q)
#for i in range(0, l-2, 2):	
#	qc.x(i)

qc.cz(0, 2)
qc.cz(1, 3)
#add more gates

oracle = qc.to_gate()
oracle.name = "U$_\omega$"
#print(oracle.draw())

grover_circuit.append(oracle, value_bits[:l])


#---------------------diffuser----------------------------
#Diffuser code from qiskit documentation
def diffuser(nqubits):
    
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
    qc.h(nqubits-1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
#    print(qc.draw())
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "U_s"
    return U_s

grover_circuit.append(diffuser(l+bL), value_bits)

grover_circuit.measure_all()	#measure all qubits

print(grover_circuit.draw(output='text'))	#print the circuit



#----------------------------------simulate the circuit------------------------------
sim = Aer.get_backend('aer_simulator')		#simulator
state_vec=grover_circuit.save_statevector()
t_qc = transpile(grover_circuit, sim)	
nshots = 4096
counts = sim.run(t_qc, shots=nshots).result().get_counts()
#print(state_vec)

#-----------------get the location of the solution states------------------------------
#for one solution state
#sol_state_count = max(counts.values())
#counts_values = list(counts.values())
#sol_state_index = counts_values.index(sol_state_count)
#counts_keys = list(counts.keys())
#sol_state = counts_keys[sol_state_index]
#print(sol_state)
#print(counts)
#def output_vector(counts_keys, sol_state, array_i):
#	out_vec = []
#	ind=0
#	for i in counts_keys:
#		if i == sol_state:
#			ind = array_i.index(int(i[l-1:],2))
#			out_vec.append(bin(ind)[2:]) 
#	print(ind)
#	return out_vec
#out_vec = output_vector(counts_keys, sol_state, array_i)

#print(array_i)
#print(sol_state)

#print(out_vec)

#def superpose(out_vec):	
#	output = ''		
#	for i in out_vec:
#		output += '|'+ i + '/' + 'sqrt({})'.format(len(out_vec)) + '> '		
#	return output
	
#output = superpose(out_vec)
#print(output)


plot_histogram(counts)
plt.show()



