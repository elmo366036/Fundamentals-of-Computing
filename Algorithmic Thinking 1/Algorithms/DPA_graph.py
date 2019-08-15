'''Create DPA graphs'''


import random

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm

    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def make_complete_graph(num_nodes):
    '''Create a complete directed graph with
       the number of nodes equal to num_nodes
    '''
    if num_nodes == 1:
        return {0:set([])}

    graph = {}
    graph = {key: set() for key in range(num_nodes)} # dictionary of empty sets
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            graph[i].add(j)         # set i to j:
            graph[j].add(i)         # set j to i
    return graph
                

def DPA(n,m):
    '''runs DPA algorithm
    '''
    # create a complete directed graph of m nodes
    graph = make_complete_graph(m)

    # now add n-m nodes and connect each to m nodes, ignoring parallel connections
    i = m
    DPATrial1 = DPATrial(m)
    while i < n:
        graph[i] = DPATrial1.run_trial(m)
        i += 1

    return graph

print(make_complete_graph(5))