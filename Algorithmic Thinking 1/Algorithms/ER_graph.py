'''Create ER graph both directed and undirected'''

import random
##########################################################
# Code for creating ER undirected graph

def make_random_ugraph(num_nodes, p):
    '''Create a random undirected graph with
       the number of nodes equal to num_nodes
       Unoptimized. Creates twice as many edges
    '''
    if num_nodes == 1:
        return {0:set([])}

    graph = {}
    for i_dummy in range(num_nodes):
        for j_dummy in range (i_dummy + 1, num_nodes):
            if random.random() < p:
                if i_dummy not in graph:
                    graph[i_dummy] = set([j_dummy])
                else:
                    lst = graph[i_dummy]
                    lst.add(j_dummy)
                    graph[i_dummy] = lst

                if j_dummy not in graph:
                    graph[j_dummy] = set([i_dummy])
                else:
                    lst = graph[j_dummy]
                    lst.add(i_dummy)
                    graph[j_dummy] = lst
    return graph

def make_random_ugraph2(num_nodes, p):
    '''Another way to do it. Better!!!
       Optimized syntax and the loop only runs for half the i_j combinations
    '''
    # initialize graph to a dictionary of key:empty set
    graph = {key: set() for key in range(num_nodes)} # dictionary of empty sets
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < p:
                graph[i].add(j)         # set i to j
                graph[j].add(i)         # set j to i
    return graph

def make_random_dgraph(num_nodes, p):
    '''Create a random directed graph with
       the number of nodes equal to num_nodes
       Not Optimized
    '''
    if num_nodes == 1:
        return {0:set([])}

    graph = {}
    for i_dummy in range(num_nodes):
        for j_dummy in range (num_nodes):
            if i_dummy != j_dummy:
                if random.random() < p:
                    if i_dummy not in graph:
                        graph[i_dummy] = set([j_dummy])
                    else:
                        lst = graph[i_dummy]
                        lst.add(j_dummy)
                        graph[i_dummy] = lst                                            
    return graph

def make_random_dgraph2(num_nodes, p):
    '''Another way to do it. Better!!!
       OPtimized syntax and the loop only runs for half the i_j combinations 
    '''
    # initialize graph to a dictionary of key:empty set
    graph = {key: set() for key in range(num_nodes)} #dictionary of empty sets
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < p:
                graph[i].add(j)         #set i to j
            if random.random() < p:
                graph[j].add(i)
    return graph

count = 0
#print(len(make_random_ugraph2(1239, .004)))
for i in make_random_ugraph(1239, .0039).values():
    count += len(i)
print(count/2)

print(make_random_dgraph2(4,.2))