'''BFS, connected components, and a resiliency tested that removes nodes 
   one at a time and checks for connected components 
'''

def bfs_visited(ugraph, start_node):
    '''bfs that tracks visited nodes'''

    visited = set()
    visited.add(start_node)
    queue = collections.deque()
    queue.append(start_node)

    if start_node not in ugraph:
        return visited

    while len(queue) != 0:
        node = queue.pop()
        neighbors = ugraph[node]
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

def cc_visited(ugraph):
    '''connected components
    '''

    remaining_nodes = set(ugraph.keys())
    connected_components_list = []

    while len(remaining_nodes) > 0:
        node = remaining_nodes.pop()
        connected_components = bfs_visited(ugraph, node)
        if connected_components not in connected_components_list:
            connected_components_list.append(connected_components)
        remaining_nodes.difference(connected_components)

    return connected_components_list

def largest_cc_size(ugraph):
    '''largest connected graph size
    '''
    largest_size = 0
    connected_components = cc_visited(ugraph)
    for idx in connected_components:
        if len(idx) > largest_size:
            largest_size = len(idx)

    return largest_size

def compute_resilience(ugraph, attack_order):
    '''removes attack_order nodes from ugraph and
       computes largest connected component size
    '''
    largest_cc_sizes = []
    new_graph = copy_graph(ugraph)
    largest_cc_sizes.append(largest_cc_size(ugraph))

    for node in attack_order:
        for key, values in ugraph.items():
            if node == key:
                new_graph.pop(key)
            if node in values:
                values.remove(node)
                new_graph[key] = values
        largest_cc_sizes.append(largest_cc_size(new_graph))
    return largest_cc_sizes