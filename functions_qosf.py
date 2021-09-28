import math
def clause_matrix_0(N):
	clause = [0]*N
	for i in range(0,N):
		clause[i]=i
	return clause
	
def clause_matrix_1(N):
	clause=[0]*N
	for i in range(0,N):
		clause[i]=i+1
	return clause	
	
def solution_states(n):
	state_1=0
	state_2=0
	for i in range(0,n-1,2):
		state_1= state_1 + 2**(i+n%2)
	state_2 = 2**n - 1 - state_1
	solution_states = [state_1, state_2]
	return solution_states
	
def binarize(array_i, l):
	array_b = [0]*len(array_i)
	for i in range(0, len(array_i)):
		array_b[i]=f'{array_i[i]:0{l}b}'
#		array_b[i]=bin(array_i[i])		
	return array_b
	
def inversion(array_i, N):
	for i in range(0,len(array_i)):
		array_i[i] = N-1 - array_i[i]
	return array_i
	
def sat(all_combinations,l, bL):
	L2 = ""
	temp = []
	clause = clause_matrix_1(l+bL)	#To create the constraints/clauses
	m = max(clause)
	for i in range(0, len(all_combinations)):
		k=0
		j=all_combinations[i]
		temp = [int(i)+1 for i in range(m)]
		while k<=l+bL-1:
			if j%(2)==0:
				temp[k] = (temp[k])*(-1)
			stri = str(temp[k]) + str(' ')
			L2 += (stri)
			j = j//2
			k = k+1
		L2 += '0 \n'
	return L2

def entangle(array_i, l, bL):
	highest = max(array_i)

	addresses = clause_matrix_0(len(array_i))

	addresses_bin = binarize(addresses,bL)

	com_state = [0]*len(array_i)
	array_b = binarize(array_i, l)
	for i in range(len(array_i)):
		com_state[i] = str(addresses_bin[i]) + str(array_b[i])

	return com_state
	
def init_vector(array_i, N):	#initialisation vector; wont work for repeated SOLUTIONS, works for repeated input
	norm = 0
	init_vec = [0.]*N	#equal superposition intialisation vector	
	for i in array_i:
		init_vec[i]=1.0
	print(init_vec)
	for i in init_vec:
		norm = norm + i
#	print(norm)
	for i in range(len(init_vec)):
		init_vec[i] = init_vec[i]/math.sqrt(norm)
	return init_vec	
	
