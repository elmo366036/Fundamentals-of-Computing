######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    # need a deep copy, not a shallow copy!!!
    new_cluster_list = copy.deepcopy(cluster_list)
    
    while len(new_cluster_list) > num_clusters:   
        new_cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        closest_pair = fast_closest_pair(new_cluster_list)
        point_a = closest_pair[1]
        point_b = closest_pair[2]
        new_cluster_list[point_a].merge_clusters(new_cluster_list[point_b])
        del new_cluster_list[point_b]

    return new_cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters

    Algorithm
        Initialize old cluster using large population counties 
        For number of iterations 
          Initialize the new clusters to be empty 
          For each county 
              Find the old cluster center that is closest 
              Add the county to the corresponding new cluster 
          Set old clusters equal to new clusters 
          Return the new clusters
    """
    centers = []
    
    # initialize k centers using largest populations
    temp_cluster_list = list(cluster_list)
    temp_cluster_list.sort(key = lambda cluster: cluster.total_population(), reverse = True)      
    for count in range(num_clusters):
        centers.append(temp_cluster_list[count])
    
    # for each iteration num_iterations. each iteration will update centers
    for dummy_i in range(num_iterations):
        # create k empty sets of clusters (alg_cluster.Cluster)
        temp_cluster_list = [alg_cluster.Cluster(set([]), 0,0,0,0) for dummy_i in range(num_clusters)] # empty set of k clusters
        
        # for each pair in cluster_list, find the center closest to it
        for cluster in cluster_list:
            min_dist = float('inf')
            min_center_pos = 0
            center_index = 0
            for center in centers:
                if center.distance(cluster) < min_dist:
                    min_dist = center.distance(cluster)
                    min_center_pos = center_index
                center_index += 1
            # merge the cluster with the center that it is closest to
            # this call recalculates the center position
            temp_cluster_list[min_center_pos].merge_clusters(cluster)
         # overwrite the centers list with the temp one 
        centers = list(temp_cluster_list)           
            
    return centers