'''Week 2
   http://www.codeskulptor.org/#user45_AtEVRULics_10.py
'''


EX_GRAPH0 = {0:set([1,2]), 1:set([]), 2:set([])}
EX_GRAPH1 = {0:set([1,4,5]), 1:set([2,6]), 2:set([3]),
             3:set([0]), 4:set([1]), 5:set([2]), 6:set([])}
EX_GRAPH2 = {0:set([1,4,5]), 1:set([2,6]), 2:set([3,7]),
             3:set([7]), 4:set([1]), 5:set([2]), 6:set([]),
             7:set([3]), 8:set([1,2]), 9:set([0,3,4,5,6,7])}

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


#rint make_complete_graph(4)
print compute_in_degrees(EX_GRAPH2)
print in_degree_distribution(EX_GRAPH2)
