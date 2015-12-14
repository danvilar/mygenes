#===============================================================================
# My Genes v3.0.0 (04/Dezembro/2015)
# coded by: Daniel Vilar
# email: dvjorge@fc.ul.pt
# 15/October/2013
#===============================================================================

import numpy as np

prob_duplic = 0.5
prob_elim = 0.5
prob_mut = 0.5
it_steps = 5

class Graph:
	def __init__(self, default_nodes, inter_nodes):
		
		self.inter_nodes = np.array([i for i in xrange(inter_nodes)], dtype=np.int)
		self.default_nodes = np.array([i for i in xrange(default_nodes)]+[i for i in xrange(default_nodes)], dtype=np.int)
		self.default_nodes_n = default_nodes
		self.inter_nodes_n = inter_nodes
		self.edges = np.zeros((default_nodes*2+inter_nodes,default_nodes*2+inter_nodes), dtype=np.int)
	
	def duplic_nodes(self):
		prob_array = np.random.rand(self.inter_nodes.size)<= prob_duplic
		to_duplic = np.extract(prob_array, np.arange(self.inter_nodes.size))
		to_duplic += self.default_nodes_n*2
		
		#add new node rows to edges
		to_add_v = np.array([self.edges[i,:] for i in to_duplic])
		self.edges = np.vstack((self.edges, to_add_v))
		
		#add new node columns to edges
		to_add_h = np.array([self.edges[:,i] for i in to_duplic])
		self.edges = np.hstack((self.edges, to_add_h.transpose()))
		
		#add new nodes to inter_nodes array
		self.inter_nodes = np.append(self.inter_nodes, np.array([self.inter_nodes_n + i for i in xrange(to_duplic.size)]))
		#get the new id number
		self.inter_nodes_n += to_duplic.size

	def elim_nodes(self):
		prob_array = np.random.rand(self.inter_nodes.size)<= prob_elim
		to_elim = np.extract(prob_array, np.arange(self.inter_nodes.size))
		
		#remove nodes from inter_nodes array
		self.inter_nodes = np.delete(self.inter_nodes,to_elim)
		to_elim += self.default_nodes_n*2
		
		#remove mask and remove nodes from edges
		mask = np.ones(self.edges.shape, dtype = bool)
		mask[:,to_elim] = False
		mask[to_elim,:] = False
		self.edges = self.edges[mask].reshape(len(self.edges)-len(to_elim), len(self.edges)-len(to_elim))
		
	def mut_edges(self):
		pass
		
	def stim(self):
		pass
		
	def nodes(self):
		return np.append(self.default_nodes, self.inter_nodes)

G = Graph(6,6)
G.elim_nodes()
