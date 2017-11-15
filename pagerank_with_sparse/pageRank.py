import operator
import math, random, sys, csv 
from utils import parse, print_results
import networkx as nx
import matplotlib.pyplot as plt
from igraph import *
import scipy as sp
import numpy as np
import time

class PageRank:
    def __init__(self, graph, directed):
        self.graph = graph
        self.V = len(self.graph)
        self.d = 0.85
        self.directed = directed
        self.ranks = dict()
    
    def rank(self):
        for key, node in self.graph.nodes(data=True):
            if self.directed:
                self.ranks[key] = 1/float(self.V)
            else:
                self.ranks[key] = node.get('rank')
	start = time.time()
        for _ in range(15):
            for key, node in self.graph.nodes(data=True):
                rank_sum = 0
                curr_rank = node.get('rank')
                if self.directed:
                    neighbors = self.graph.out_edges(key)
                    for n in neighbors:
                        outlinks = len(self.graph.out_edges(n[1]))
                        if outlinks > 0:
                            rank_sum += (1 / float(outlinks)) * self.ranks[n[1]]
                else: 
                    neighbors = self.graph[key]
                    for n in neighbors:
                        if self.ranks[n] is not None:
                            outlinks = len(self.graph.neighbors(n))
                            rank_sum += (1 / float(outlinks)) * self.ranks[n]
            
                # actual page rank computation
                self.ranks[key] = ((1 - float(self.d)) * (1/float(self.V))) + self.d*rank_sum
	time_taken = time.time() - start
	print "Time taken is: "+ str(time_taken)+" seconds.\n"
        return p

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Expected input format: python pageRank.py <data_filename> <directed OR undirected>'
    else:
        filename = sys.argv[1]
        isDirected = False
        if sys.argv[2] == 'directed':
            isDirected = True

        graph = parse(filename, isDirected)
        p = PageRank(graph, isDirected)
        p.rank()

        sorted_r = sorted(p.ranks.iteritems(), key=operator.itemgetter(1), reverse=True)
	#print len(sorted_r)
	scores = []
	nodelist = []
        for tup in sorted_r:
            #print '{0:30} :{1:10}'.format(str(tup[0]), tup[1])
	    nodelist.append(tup[0])
	    scores.append(tup[1])
	#print scores
	matr = nx.adjacency_matrix(p.graph)
	nmatr = matr.todense()
	slicedmatr = nmatr[0:30,0:30].tolist()
	adj = Graph.Adjacency(slicedmatr)
	adj.vs["name"] = nodelist
	adj.vs["attr"] = ["%.3f" % k for k in scores]
	minim = min(scores)
	#print minim
	layout = adj.layout("kk")
	visual_style = {}
	visual_style["vertex_size"] = [scores[i]*10000 for i in range(0,30)]
	visual_style["vertex_label"] = [(adj.vs["name"][i], adj.vs["attr"][i]) for i in range(0,30)]
	visual_style["layout"] = layout
	visual_style["bbox"] = (1000, 1000)
	visual_style["margin"] = 200
	plot(adj, **visual_style)	
