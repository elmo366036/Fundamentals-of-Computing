'''Week 2
http://www.codeskulptor.org/#user45_AtEVRULics_11.py
'''
import math

"""
Constants for part a
"""
EX_GRAPH0 = {0:set([1,2]), 1:set([]), 2:set([])}
EX_GRAPH1 = {0:set([1,4,5]), 1:set([2,6]), 2:set([3]),
             3:set([0]), 4:set([1]), 5:set([2]), 6:set([])}
EX_GRAPH2 = {0:set([1,4,5]), 1:set([2,6]), 2:set([3,7]),
             3:set([7]), 4:set([1]), 5:set([2]), 6:set([]),
             7:set([3]), 8:set([1,2]), 9:set([0,3,4,5,6,7])}


"""
Provided code for Application portion of Module 1

Imports physics citation graph
"""

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def make_complete_graph(num_nodes):
    '''Create a complete directed graph with
       the number of nodes equal to num_nodes
    '''
    if num_nodes == 1:
        return {0:set([])}

    graph = {}
    for i_dummy in range(0, num_nodes):
        for j_dummy in range (0, num_nodes):
            if i_dummy != j_dummy:
                if graph.has_key(i_dummy) == False:
                    graph[i_dummy] = set([j_dummy])
                else:
                    lst = graph[i_dummy]
                    lst.add(j_dummy)
                    graph[i_dummy] = lst
    return graph

def compute_in_degrees(digraph):
    '''Creats a dictionary of in degrees with all nodes
    '''
    graph = {}
    for node_a in digraph.keys():
        # put node_a into graph if not already there
        # and initialtize to 0
        if graph.has_key(node_a) == False:
            graph[node_a] = 0
        # get node_bs and count number of ingresses to them
        node_b_tuple = digraph[node_a]
        for node_b in node_b_tuple:
            if graph.has_key(node_b) == False:
                graph[node_b] = 1
            else:
                graph[node_b] += 1
    return graph

def in_degree_distribution(digraph):
    '''Creates a dictionary of the distribution of in-degrees
    '''
    graph = {}
    in_degrees = compute_in_degrees(digraph)
    nodes = in_degrees.keys()
    for node in nodes:
        if graph.has_key(in_degrees[node]) == False:
            graph[in_degrees[node]] = 1
        else:
            graph[in_degrees[node]] += 1


    return graph

def normalize(in_graph):
    '''Normalizes the in_degree_distribution
    '''
    graph = {}
    total = 0.0
    #sum = 0.0
    for in_degree in in_graph.keys():
        total += in_graph[in_degree]
    for in_degree in in_graph.keys():
        graph[in_degree] = in_graph[in_degree] / total
    #for in_degree in graph.keys():
    #    sum += graph[in_degree]
    #print "sum", sum
    return graph

def logify(in_graph):
    '''Creates a log of the in_graph
    '''
    graph = {}
    for in_degree in in_graph.keys():
        log_in_degree = math.log(in_degree, 10)
        log_dist = math.log(in_graph[in_degree], 10)
        graph[log_in_degree] = log_dist
    return graph

# Part A
#print make_complete_graph(4)
#print compute_in_degrees(EX_GRAPH2)
#print in_degree_distribution(EX_GRAPH2)

# Part B
citation_graph = load_graph(CITATION_URL)
in_degree_dist = in_degree_distribution(citation_graph)
normalized_in_dist = normalize(in_degree_dist)
log_norm_in_dist = logify(normalized_in_dist)

import simpleplot
simpleplot.plot_scatter("Application #1: Question 1", 400, 300, 'log # in-degrees (number of citations)', 'log dist in_degrees (fraction of citations)', [log_norm_in_dist])
