

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.  
    
    Brute Force     
    """
    
    ans = (float('inf'),-1,-1)
    for idx_i in range(len(cluster_list)):
        for idx_j in range(idx_i + 1, len(cluster_list)):
            distance = pair_distance(cluster_list, idx_i, idx_j)                
            if distance[0] < ans[0]:
                ans = distance
    return ans


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    ans = (float('inf'),-1,-1)
    num_points = len(cluster_list)
    
    if num_points <= 3:
        ans = slow_closest_pair(cluster_list)
    else:
        mid = num_points / 2 
        ans_left = fast_closest_pair(cluster_list[:mid])        # closest left half
        ans_r = fast_closest_pair(cluster_list[mid:])           # closest right half  
        ans_right = (ans_r[0], ans_r[1] + mid, ans_r[2] + mid)  # update indices for ans_r        
        ans_lr = min([ans_left, ans_right], key = lambda t: t[0])  

        # determine min distance of two points spanning the mid line
        mid_line = .5*(cluster_list[mid].horiz_center() + cluster_list[mid - 1].horiz_center())
        ans_mid = closest_pair_strip(cluster_list, mid_line, ans_lr[0])

        ans = min([ans_lr, ans_mid], key = lambda t: t[0]) 

    return ans


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """  
    # create a list of clusters that meet specific criteria
    midline_list = []
    for cluster in cluster_list:
        if math.fabs(cluster.horiz_center() - horiz_center) < half_width:
            midline_list.append(cluster)    
    
    # sort them
    midline_list.sort(key = lambda cluster: cluster.vert_center())

    # iterate through the set and find the minimum
    ans = (float('inf'), -1 ,-1)
    num_points = len(midline_list)
    
    for idx_u in range(num_points - 1):
        for idx_v in range(idx_u + 1, min(idx_u + 3, num_points - 1) + 1):
            distance = pair_distance(midline_list, idx_u, idx_v)                
            if distance[0] < ans[0]:
                ans = distance  
    
    # convert the indices in midline_list back to cluster_list if there are any
    if ans != (float('inf'), -1 ,-1): 
        index_1 = cluster_list.index(midline_list[ans[1]])
        index_2 = cluster_list.index(midline_list[ans[2]])   
        dist = ans[0]
        ans = (dist, min(index_1, index_2), max(index_1, index_2))
    
    return ans