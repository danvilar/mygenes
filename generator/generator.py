#===============================================================================
# My Genes Generator v1.1.1 (15/December/2015)
# coded by: Daniel Vilar
# email: dvjorge@fc.ul.pt
# 07/December/2015
#===============================================================================

#Python modules import
import pickle #Data Dumper
import random #module to make random choices
import numpy as np #mathematical module
import scipy.spatial.distance as sp #Jaccard, etc...
from collections import Counter #Counters
from os import listdir, path, makedirs
from sys import argv
import time

run_name = str(argv[1]) #run name
n_cells = int(argv[2]) #cells per generation
n_inter_nodes = int(argv[3]) #number of inter nodess
n_edges_create = int(argv[4]) #number of edges to create
it_steps = int(argv[5]) #Steps of the boolean analysis
env_set = str(argv[6]) #Enviornment set name (must be *.env)

# Data folder
if not path.exists(run_name):
	makedirs(run_name)

params = open('%s/params.txt' %run_name,'w',0)
params.write('''Parameter\tValue
n_cells\t\t%s
n_nodes\t\t%s
n_edges\t\t%s
it_steps\t%s
env_set\t\t%s''' %(n_cells, n_inter_nodes, n_edges_create, it_steps, env_set))
params.close()

# Environment loader
def loadEnv():
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
					environment[env_counter][0].append('I%s' %node_counter)
			for outnode in in_out[1].split(','):
				environment[env_counter][1].append(int(outnode))
	env_file.close()

	default_nodes, II, OO = [], [], []
	for a in xrange(n_inputs):
		default_nodes.append('I%s' %(a+1))
		II.append('I%s' %(a+1))
	for a in xrange(n_outputs):
		default_nodes.append('O%s' %(a+1))
		OO.append('O%s' %(a+1))

	return environment, default_nodes, II, OO

class new_cell:
	'''In this class, there are found every variable and
	functions of a cell's network.'''

	def __init__(self, (n_counter, newnodes, newedges)):
		self.n_counter = n_counter #Node id counter
		self.G = [newnodes[:],newedges[:]]

	def getAtrib(self):
		return self.n_counter, self.G[0], self.G[1]

	def add_edges(self):
		new_graph = []
		copy_nodes = self.G[0][:]

		for node in self.G[0]:
			for e in II:
				new_graph.append((e,node))

			for n in copy_nodes:
				if bool(random.getrandbits(1)) == True:
					new_graph.append((n,node))
				else:
					new_graph.append((node,n))

			for f in OO:
				new_graph.append((node,f))

		self.G[1] = random.sample(new_graph,n_edges_create)

	def all_operations(self):
		'''Ordered oprations'''
		self.add_edges()
		return self.stim()

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

			test_array = [[0 for n in OO],environment[envx][1][:]] # test array created

			for actenv in environment[envx][0]: # Initial stimuli
				boolean_nodes[actenv] = True

			temp_factive_nodes, temp_factive_edges = [], []
			spread_nodes = [] #To spread nodes

			for step in xrange(it_steps): #For each step defined above
				for q in boolean_nodes: # For each node, if it's set to True and it has not been spread yet
					if q not in spread_nodes and boolean_nodes[q] == True:
						spread_nodes.append(q)
						try:
							for qq in edges_dic[q]:
								boolean_nodes[qq] = True
								if qq not in temp_factive_nodes and qq[0] != 'O':
									temp_factive_nodes.append(qq)
								if (q,qq) not in temp_factive_edges:
									temp_factive_edges.append((q,qq))
						except:
							pass

			[factive_nodes.append(r) for r in temp_factive_nodes]
			[factive_edges.append(r) for r in temp_factive_edges]

			for node in boolean_nodes:
					if node[0] == 'O' and boolean_nodes[node] == True:
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

		total_of_nodes = len(self.G[0])
		total_of_edges = len(self.G[1])

		print >> report, '%s\t%s\t%s' %(fit_total, node_mod, edge_mod)

		return fit_total, node_mod, edge_mod, total_of_nodes, total_of_edges

#Timer (total simulation time)
start_time = time.time()

environment, default_nodes, II, OO = loadEnv()

#Report Start
report = open('%s/Report_generator.txt' %run_name, 'w', 0)
print >> report, 'Fitness\tMod_Node\tMod_edge'

#Cell's Birth
new_nodes = ['N%s' %i for i in xrange(n_inter_nodes)]
population = [new_cell((len(new_nodes)-1,new_nodes,[])) for i in xrange(n_cells)] #list of the different objects/cells

print '%s cells were born! Congratulations!\n' %n_cells

#Scripting
print time.time() - start_time, "seconds"
fits,nodes_modularity,edges_modularity, nodes_total,edges_total = zip(*[x.all_operations() for x in population])

pickle.dump([x.getAtrib() for x in population], open('%s/dataset.bin' %run_name, 'wb'))
print "Finished in %s total seconds." %(time.time() - start_time) #total simulation time
