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
from functions_qosf import clause_matrix_0, solution_states, binarize, inversion, sat, clause_matrix_1, entangle, init_vector

#array_i = [1, 2, 3, 4] #input array

#array_i = list(np.random.randint(low = 0, high = 7, size = 4, dtype = np.int64))
if __name__ == "__main__":
	enter = """\nEnter input array"""
	input_array = [int(i) for i in input(enter).split()]
    
array_i = input_array #input array
L=len(array_i)		#length of input array
highest = max(array_i)	
print(highest)
#l = math.ceil(math.log(highest,2))
l_b = bin(highest)[2:]
l = len(l_b)
print(l)
bL_b = bin(len(array_i)-1)[2:]
bL = len(bL_b)	
print(bL)
N = 2**l
#print(highest)
#print(l)

#-------------------create sat file-----------------------------------
clauses_0 = clause_matrix_0(2**(l+bL))	#all numbers from 0 to N-1
solution_states = solution_states(l)


#print(all_combinations)
sol_state_1_1 = [solution_states[0]]*(len(array_i))	#to generate the entanglement between solution state and their addresses
sol_state_2_1 = [solution_states[1]]*(len(array_i))

sol_state_1_2 = entangle(sol_state_1_1,l,bL)
sol_state_2_2 = entangle(sol_state_2_1,l,bL)

print('sol_state_1_2 = {}'.format(sol_state_1_2))
print('sol_state_2_2 = {}'.format(sol_state_2_2))
def remove(sol_state_1_2, all_combinations):
	for i in sol_state_1_2:
		all_combinations.remove(int(i,2))
	return all_combinations
clauses_1 = remove(sol_state_1_2, clauses_0)	#remove solution states
clauses = remove(sol_state_2_2, clauses_1)	#final all_combinations
print(clauses)

#create dimacs file
path = '/home/saniya/Desktop/QOSF'  

file = 'newsat.dimacs'

with open(os.path.join(path, file), 'w') as fp:
    pass
    
file1 = open("newsat.dimacs","w")

L1 = ["c QOSF DIMACS-CNF SAT \n", "p cnf {} {} \n".format(l+bL, 2**(l+bL)-2**(bL+1))]

L2 = sat(clauses, l, bL)

file1.writelines(L1)
file1.writelines(L2)
file1.close()		


#------------------------------------------------------------------------

init_vec_b = entangle(array_i,l, bL)
def bin2int(init_vec_b):
	init_vec=[0]*len(init_vec_b)
	for i in range(len(init_vec_b)):
		init_vec[i] = int(init_vec_b[i],2)
	print(init_vec)
	return init_vec	#indices
init_vec_d = bin2int(init_vec_b)	#decimal values of |x,w_x> 
init_vec = init_vector(init_vec_d, 2**(l+bL))	#normalised initialisation vector 
#init_vec = [1/np.sqrt(2**(l+bL))]*(2**(l+bL))
print('init_vec ={}'.format(init_vec))
grover_circuit = QuantumCircuit(l+bL)	#make circuit

grover_circuit.initialize(init_vec)	#initialise circuit

oracle = PhaseOracle.from_dimacs_file('newsat.dimacs')	


grover_operator = GroverOperator(oracle)  


grover_circuit = grover_circuit.compose(grover_operator)
grover_circuit.measure_all()	#measure all qubits
print(grover_circuit.draw(output='text'))	#print the circuit and gates

sim = Aer.get_backend('aer_simulator')		#simulator
t_qc = transpile(grover_circuit, sim)	
shotsy = 4096
counts = sim.run(t_qc, shots=shotsy).result().get_counts()

#for one solution state
sol_state_count = max(counts.values())
counts_values = list(counts.values())
sol_state_index = counts_values.index(sol_state_count)
counts_keys = list(counts.keys())
sol_state = counts_keys[sol_state_index]
print(sol_state)
print(counts)
def output_vector(counts_keys, counts_values, shots, sol_state, array_i):
	out_vec = []
	ind=0
	for i in counts_keys:
		if i == sol_state:
			ind = array_i.index(int(i[bL:],2))
			out_vec.append(bin(ind)[2:]) 
	print(ind)
	return out_vec
out_vec = output_vector(counts_keys, counts_values, shotsy, sol_state, array_i)

print(array_i)
#print(sol_state)

print(out_vec)

def superpose(out_vec):	
	output = ''		
	for i in out_vec:
		output += '|'+ i + '/' + 'sqrt({})'.format(len(out_vec)) + '> '
		
	return output
	
output = superpose(out_vec)
print(output)
plot_histogram(counts)
plt.show()





