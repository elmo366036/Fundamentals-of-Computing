
import alg_cluster
import alg_project3_solution as process_cluster
import time
import random
import matplotlib.pyplot as plt

def gen_random_clusters(num_clusters):
    cluster_list = []
    for i in range(num_clusters):
        rand_x = random.uniform(0,1) * random.choice([-1,1])
        rand_y = random.uniform(0,1) * random.choice([-1,1])
        cluster = alg_cluster.Cluster(set([]), rand_x ,rand_y, 0, 0)              
        cluster_list.append(cluster)
    return cluster_list

def timed_run():
    
    slow_times = []
    fast_times = []
    
    for i in range(2,201):
        cluster_list = gen_random_clusters(i)
        
        start_time = time.time()
        process_cluster.slow_closest_pair(cluster_list)
        end_time = time.time()
        ellapsed_time = end_time - start_time
        slow_times.append(ellapsed_time)
        
        start_time = time.time()
        process_cluster.fast_closest_pair(cluster_list)
        end_time = time.time()
        ellapsed_time = end_time - start_time
        fast_times.append(ellapsed_time)
    
    return slow_times, fast_times
       
slow_times, fast_times = timed_run()

n = range(2,201)
plt.plot(n,slow_times)
plt.plot(n,fast_times)
plt.legend(['slow_closest_pair', 'fast_closest_pair'], loc='upper left')
plt.title('Comparing efficiency of slow_closest_pair and fast_closest_pair')
plt.ylabel('Time (s)')
plt.xlabel('Number of clusters')
plt.show()
