#===============================================================================
# My Genes v2.2.5 (17/Novembro/2015)
# coded by: Daniel Vilar
# email: dvjorge@fc.ul.pt
# 15/October/2013
#===============================================================================

#Python modules import
import pickle #Data Dumper
import random #module to make random choices
import numpy as np #mathematical module
import scipy.spatial.distance as sp #Jaccard, etc...
from collections import Counter #Counters
from os import listdir, path, makedirs
from sys import argv


#Comment below to run with shell arguments
#Uncomment below to preset the variables

#List Environment Sets
# print '-- Environment Sets --'
# for fname in listdir('env'):
#	 print fname
# print ''

#Probabilities and Parameters
# run_name = 'teste'
# run_name = raw_input("Run name: ")
# n_cells = 1000 #cells per generation
# n_generations = 100 #generations number
# prob_duplic = 0.005 #Node duplication probability
# prob_elim = 0.005 #Node elimination probability
# prob_delta = 0.005 #Edge creation probability
# prob_alpha = 0.005 #Edge elimination probability
# it_steps = 5 #Steps of the boolean analysis
# replicas = 2 #Number of replicas
# env_set = raw_input("Environment set: ")


#Comment below to preset the variables
#Uncomment below to run with shell arguments

run_name = str(argv[1])
n_cells = int(argv[2]) #cells per generation
n_generations = int(argv[3]) #generations number
prob_duplic = float(argv[4]) #Node duplication probability
prob_elim = float(argv[5]) #Node elimination probability
prob_delta = float(argv[6]) #Edge creation probability
prob_alpha = float(argv[7]) #Edge elimination probability
it_steps = int(argv[8]) #Steps of the boolean analysis
replicas = int(argv[9]) #Number of replicas
env_set = str(argv[10])
select_fit = int(argv[11]) #1 for fitness selection, 0 for no criteria

# Data folder
if not path.exists(run_name):
	makedirs(run_name)

params = open('%s/params.txt' %run_name,'w',0)
print >> params, 'Parameter\tValue'
print >> params, 'n_cells\t\t%s' %n_cells
print >> params, 'n_generations\t%s' %n_generations
print >> params, 'prob_duplic\t%s' %prob_duplic
print >> params, 'prob_elim\t%s' %prob_elim
print >> params, 'prob_delta\t%s' %prob_delta
print >> params, 'prob_alpha\t%s' %prob_alpha
print >> params, 'it_steps\t%s' %it_steps
print >> params, 'replicas\t%s' %replicas
print >> params, 'env_set\t\t%s' %env_set
print >> params, 'select_fit\t\t%s' %select_fit



# Environment loader
env_file = open('env/%s' %env_set)
env_counter = 0
environment = {}
for line in env_file:
	line = line.strip().split(':')
	if line[0] == '@input':
		n_inputs = int(line[1])
	elif line[0] == '@output':
		n_outputs = int(line[1])
	elif line[0] == '@env':
		env_counter += 1
		environment[env_counter] = list()
		environment[env_counter].append(list())
		environment[env_counter].append(list())
		in_out = line[1].strip().split(';')
		node_counter = 0
		for innode in in_out[0].split(','):
			node_counter += 1
			if innode == '1':
				environment[env_counter][0].append('E%s' %node_counter)
		for outnode in in_out[1].split(','):
			environment[env_counter][1].append(int(outnode))				  
env_file.close()

print 'Parameter\tValue'
print 'n_cells\t\t%s' %n_cells
print 'n_generations\t%s' %n_generations
print 'prob_duplic\t%s' %prob_duplic
print 'prob_elim\t%s' %prob_elim
print 'prob_delta\t%s' %prob_delta
print 'prob_alpha\t%s' %prob_alpha
print 'it_steps\t%s' %it_steps
print 'replicas\t%s' %replicas
print 'env_set\t\t%s' %env_set

# Default nodes (input/output nodes)
default_nodes, EE, FF = [], [], []
for a in range(n_inputs):
	default_nodes.append('E%s' %(a+1))
	EE.append('E%s' %(a+1))
for a in range(n_outputs):
	default_nodes.append('F%s' %(a+1))
	FF.append('F%s' %(a+1))

class new_cell:
	'''In this class, there are found every variable and
	functions of a cell's network.'''

	def __init__(self,n_counter):
		self.n_counter = n_counter #Node id counter
		self.G = [[],[]]

	def all_operations(self):
		'''All operations were put in a single function
		to improve performance. The order is: duplication,
		elimination and mutation.'''

		'''Duplication:
		iteration of all nodes duplicating them with a
		certain probability. All of the edges are kept'''

		copy_nodes = self.G[0][:]
		copy_edges = self.G[1][:]

		for node in copy_nodes:
			if np.random.random_sample() <= prob_duplic:
				self.n_counter += 1
				self.G[0].append('N%s' %self.n_counter)

				for a in copy_edges:
					if a[0] == node:
						self.G[1].append(('N%s' %self.n_counter,a[1]))

					elif a[1] == node:
						self.G[1].append((a[0],'N%s' %self.n_counter))
						
		'''Elimination:
		iteration of all nodes eliminating them with acertain probability.'''

		if len(self.G[0]) > 1:
			elim_list = []
			elim_edge_list = []
			for node in self.G[0]:
				if np.random.random_sample() <= prob_elim:
					elim_list.append(node)
					for no in self.G[1]:
						if no[0] == node or no[1] == node:
							elim_edge_list.append(no)

			self.G[0] = [x for x in self.G[0] if x not in elim_list]
			self.G[1] = [x for x in self.G[1] if x not in elim_edge_list]
		else:
			pass

		''' Mutation:
		Creates a new graph with random edges
		and the semantic distance between this
		graph and the original one is the mutation
		result '''

		new_graph = []
		copy_nodes = self.G[0][:]

		for node in self.G[0]:
			for e in EE:
				if np.random.random_sample() <= prob_delta and (e,node) not in self.G[1]:
					new_graph.append((e,node))
				elif np.random.random_sample() <= prob_alpha and (e,node) in self.G[1]:
					new_graph.append((e,node))
			for n in copy_nodes:
				if np.random.random_sample() <= prob_delta and n != node and ((n,node) not in self.G[1] or (node,n) not in self.G[1]):
					if bool(random.getrandbits(1)) == True:
						new_graph.append((n,node))
					else:
						new_graph.append((node,n))
				elif np.random.random_sample() <= prob_alpha and n != node and (n,node) in self.G[1]:
					new_graph.append((n,node))
				elif np.random.random_sample() <= prob_alpha and n != node and (node,n) in self.G[1]:
					new_graph.append((node,n))

			for f in FF:
				if np.random.random_sample() <= prob_delta and (node,f) not in self.G[1]:
					new_graph.append((node,f))
				elif np.random.random_sample() <= prob_alpha and (node,f) in self.G[1]:
					new_graph.append((node,f))


		self.G[1] = [(x,y) for (x,y) in new_graph if (x,y) not in self.G[1] and (y,x) not in self.G[1]] + [(x,y) for (x,y) in self.G[1] if (x,y) not in new_graph and (y,x) not in new_graph]


	def stim(self):
		''' Converts the graph to a boolean network
		and calculates the fit in all environment'''

		# Contrucao do dicionario e string de ligacoes
		edges_dic, boolean_nodes, factive_nodes, factive_edges = {}, {}, [], []
		fit_total, node_mode, edge_mod = 1.0, 0.0, 0.0

		for lig in self.G[1]:
			try:
				edges_dic[lig[0]].append(lig[1])
			except:
				edges_dic[lig[0]] = []
				edges_dic[lig[0]].append(lig[1])

		for envx in environment: #For each environment...
			for noda in self.G[0]:
				boolean_nodes[noda] = False
			for noda in default_nodes:
				boolean_nodes[noda] = False

			test_array = [[0 for n in FF],environment[envx][1][:]] # test array created

			for actenv in environment[envx][0]: # Initial stimuli
				boolean_nodes[actenv] = True

			temp_factive_nodes, temp_factive_edges = [], []
			spread_nodes = [] #To spread nodes

			for step in range(it_steps): #For each step defined above
				for q in boolean_nodes: # For each node, if it's set to True and it has not been spread yet
					if q not in spread_nodes and boolean_nodes[q] == True:
						spread_nodes.append(q)
						try:
							for qq in edges_dic[q]:
								boolean_nodes[qq] = True
								if qq not in temp_factive_nodes and qq[0] != 'F':
									temp_factive_nodes.append(qq)
								if (q,qq) not in temp_factive_edges:
									temp_factive_edges.append((q,qq))
						except:
							pass

			[factive_nodes.append(r) for r in temp_factive_nodes]
			[factive_edges.append(r) for r in temp_factive_edges]

			for node in boolean_nodes:
					if node[0] == 'F' and boolean_nodes[node] == True:
						test_array[0][int(node[1:])-1] = 1

			fit_parcial = (1-sp.cdist(test_array, test_array, 'jaccard')[0][1])
			fit_total = fit_total * (fit_parcial**(8./float(len(environment)))) # correction to 8 environments

		# Para evitar erros de NaN
		if len(factive_edges) == 0:
			edge_mod = 0.0
		else:
			edge_mod = float(len([kk for kk,nn in Counter(factive_edges).iteritems() if nn == 1]))/float(len(set(factive_edges)))

		if len(factive_nodes) == 0:
			node_mod = 0.0
		else:
			node_mod = float(len([kk for kk,nn in Counter(factive_nodes).iteritems() if nn == 1]))/float(len(set(factive_nodes)))
		#

		total_of_nodes = len(self.G[0])
		total_of_edges = len(self.G[1])

		return fit_total, node_mod, edge_mod, total_of_nodes, total_of_edges

#Timer (total simulation time)
import time
start_time = time.time()

for n_replica in range(replicas):
	#Cell's Birth
	population = [] #list of the different objects/cells
	for i in range(n_cells):
		ncell = new_cell(0)
		ncell.G[0] = ['N0']
		population.append(ncell)
	print '%s cells were born in replica %s! Congratulations!\n' %(n_cells,int(n_replica+1))

	#Report Start
	report = open('%s/Report%s.txt' %(run_name,int(n_replica+1)), 'w', 0)
	print >> report, 'Generation#\tFit_mean\tNode_mod_mean\tEdges_mod_mean\tNodes_mean\tEdges_mean\tFit_std\tNode_mod_std\tEdges_mod_std\tNodes_std\tEdges_std'

	#Scripting
	for ii in range(n_generations):
		print time.time() - start_time, "seconds"
		print 'Generation %i' %(int(ii)+1)

		[x.all_operations() for x in population]

		fits,nodes_modularity,edges_modularity, nodes_total,edges_total = [],[],[],[],[]
		for x1,x2,x3,x4,x5 in [x.stim() for x in population]:
			fits.append(x1)
			nodes_modularity.append(x2)
			edges_modularity.append(x3)
			nodes_total.append(x4)
			edges_total.append(x5)

		report.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(int(ii)+1,np.mean(fits),np.mean(nodes_modularity),np.mean(edges_modularity),np.mean(nodes_total),np.mean(edges_total),np.std(fits),np.std(nodes_modularity),np.std(edges_modularity),np.std(nodes_total),np.std(edges_total)))

		fit_sum = sum(fits)
		new_gen = []

		if fit_sum == 0 or select_fit == 0:

			for n in range(len(population)):
				chosen_one = random.choice(population)
				temp_graph = new_cell(chosen_one.n_counter)
				temp_graph.G[0] = chosen_one.G[0][:]
				temp_graph.G[1] = chosen_one.G[1][:]
				new_gen.append(temp_graph)

		else:

			RVF, CVF, CVF_val = [],[],0
			for fit in fits:
				RVF.append(fit/fit_sum)
				CVF_val = CVF_val + (fit/fit_sum)
				CVF.append(CVF_val)

			CVF = list(enumerate(CVF))

			for n in range(len(population)):
				rand_n = np.random.random_sample()
				for ni,e in CVF:
					if e >= rand_n:
						temp_graph = new_cell(population[ni].n_counter)
						temp_graph.G[0] = population[ni].G[0][:]
						temp_graph.G[1] = population[ni].G[1][:]
						new_gen.append(temp_graph)
						break

		population = new_gen[:]
	report.close()

	pickle.dump(population, open('%s/dataset%s.bin' %(run_name,int(n_replica+1)), 'wb'))
	print "End of replica %s in %s total seconds." %(int(n_replica+1), time.time() - start_time) #total simulation time
