'''Performs global and local alignment of two text strings
   Provide an alphabet, diag_score, off_diag_score, dash_score,
   and two strings to compare
   
   diag_score is when the characters are the same
   off_diag_score is when two characters are not the same
   dash_score is when where a character maps to a dash
   
   Includes a function to generate a null distribution  
'''   


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    ''' build scoring matrix as a dictionary of dictionaries
    '''   
    scoring_matrix = dict((dummy_a, {}) for dummy_a in alphabet)   
    scoring_matrix["-"] = {}
    
    for dummy_a in alphabet:
        for dummy_b in alphabet:
            if dummy_a == dummy_b:
                scoring_matrix[dummy_a][dummy_b] = diag_score
            else:
                scoring_matrix[dummy_a][dummy_b] = off_diag_score
        scoring_matrix["-"][dummy_a] = dash_score 
        scoring_matrix[dummy_a]["-"] = dash_score 
    scoring_matrix["-"]["-"] = dash_score     
         
    return scoring_matrix      

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    ''' compute alignment matrix
    '''
    if seq_x == '':
        return [[0]]
    alignment_matrix = [ [0] * (len(seq_y) + 1) for _ in range(len(seq_x) + 1)] # initialize 2d matrix to 0  

    scoring_matrix_copy = scoring_matrix.copy()
    
    for dummy_i in range(1,len(seq_x) + 1):
        alignment_matrix[dummy_i][0] = alignment_matrix[dummy_i - 1][0] + scoring_matrix_copy[seq_x[dummy_i - 1]]["-"]
        if global_flag == False and alignment_matrix[dummy_i][0] < 0:
            alignment_matrix[dummy_i][0] = 0 
        
    for dummy_j in range(1, len(seq_y) + 1):
        alignment_matrix[0][dummy_j] = alignment_matrix[0][dummy_j - 1] + scoring_matrix_copy["-"][seq_y[dummy_j - 1]]
        if global_flag == False and alignment_matrix[0][dummy_j] < 0:
            alignment_matrix[0][dummy_j] = 0
    
    for dummy_i in range(1,len(seq_x) + 1):
        for dummy_j in range(1, len(seq_y) + 1):
            alignment_matrix[dummy_i][dummy_j] = max(alignment_matrix[dummy_i - 1][dummy_j - 1] + 
                                                     scoring_matrix_copy[seq_x[dummy_i - 1]][seq_y[dummy_j - 1]],
                                                     alignment_matrix[dummy_i - 1][dummy_j] + 
                                                     scoring_matrix_copy[seq_x[dummy_i - 1]]["-"],
                                                     alignment_matrix[dummy_i][dummy_j - 1] +
                                                     scoring_matrix_copy["-"][seq_y[dummy_j - 1]]                                                     
                                                     )    
            if global_flag == False and alignment_matrix[dummy_i][dummy_j] < 0:
                alignment_matrix[dummy_i][dummy_j] = 0  
    
    return alignment_matrix

def compute_global_alignment(seq_x,seq_y,scoring_matrix,alignment_matrix):
    '''global alignment
    '''    
    if seq_x == "" or seq_y == "":
        return (0,"","")    
    x_pos = len(seq_x)
    y_pos = len(seq_y)
    x_res = ""
    y_res = ""    

    while x_pos > 0 and y_pos > 0:
        if alignment_matrix[x_pos][y_pos] == (alignment_matrix[x_pos - 1][y_pos - 1] +
                                             scoring_matrix[seq_x[x_pos - 1]][seq_y[y_pos - 1]]):
            x_res = seq_x[x_pos - 1] + x_res
            y_res = seq_y[y_pos - 1] + y_res       
            x_pos -= 1
            y_pos -= 1            
        else:
            if alignment_matrix[x_pos][y_pos] == (alignment_matrix[x_pos - 1][y_pos] +
                                                  scoring_matrix[seq_x[x_pos - 1]]["-"]):
                x_res = seq_x[x_pos - 1] + x_res
                y_res = "-" + y_res        
                x_pos -= 1                
            else: 
                x_res = "-" + x_res
                y_res = seq_y[y_pos - 1] + y_res        
                y_pos -= 1
    while x_pos > 0:
        x_res = seq_x[x_pos - 1] + x_res
        y_res = "-" + y_res       
        x_pos -=  1        
    while y_pos > 0:         
        x_res = "-" + x_res
        y_res = seq_y[y_pos - 1] + y_res     
        y_pos -= 1
     
    return (alignment_matrix[len(alignment_matrix) - 1][len(alignment_matrix[0]) - 1],x_res, y_res)

def compute_local_alignment(seq_x,seq_y,scoring_matrix,alignment_matrix):
    '''compute local alignment
    '''

    # find position of maximum value on alignment_matrix
    # do the global alg until alignment_matrix = 0
    
    if seq_x == "" or seq_y == "":
        return (0,"","")
    
    # find maximum value in alignment_matrix and its position
    max_score = float("-inf")
    start_pos = ()
    for idx_i in range(len(alignment_matrix) - 1, -1, -1):
        for idx_j in range(len(alignment_matrix[0]) - 1, -1, -1):
            if alignment_matrix[idx_i][idx_j] > max_score:
                max_score = alignment_matrix[idx_i][idx_j]
                start_pos = (idx_i, idx_j)

    # reuse global alignment code. start at position of max score and run until
    # alignment_matrix returns 0
    x_pos = start_pos[0]
    y_pos = start_pos[1]
    x_res = ""
    y_res = ""    

    while x_pos > 0 and y_pos > 0 and alignment_matrix[x_pos][y_pos] > 0:
        if alignment_matrix[x_pos][y_pos] == (alignment_matrix[x_pos - 1][y_pos - 1] +
                                             scoring_matrix[seq_x[x_pos - 1]][seq_y[y_pos - 1]]):
            x_res = seq_x[x_pos - 1] + x_res
            y_res = seq_y[y_pos - 1] + y_res       
            x_pos -= 1
            y_pos -= 1            
        else:
            if alignment_matrix[x_pos][y_pos] == (alignment_matrix[x_pos - 1][y_pos] +
                                                  scoring_matrix[seq_x[x_pos - 1]]["-"]):
                x_res = seq_x[x_pos - 1] + x_res
                y_res = "-" + y_res        
                x_pos -= 1               
            else: 
                x_res = "-" + x_res
                y_res = seq_y[y_pos - 1] + y_res        
                y_pos -= 1
    while x_pos > 0 and alignment_matrix[x_pos][0] > 0:
        x_res = seq_x[x_pos - 1] + x_res
        y_res = "-" + y_res       
        x_pos -=  1        
    while y_pos > 0 and alignment_matrix[0][y_pos] > 0:         
        x_res = "-" + x_res
        y_res = seq_y[y_pos - 1] + y_res     
        y_pos -= 1
    
    return (max_score, x_res, y_res)

def generate_null_distribution(seq_x,seq_y,scoring_matrix,num_trials):
    '''generates a distribution of scores for random permutations of seq_y
       for num_trials
    '''  
    scoring_dictionary = {}   
     # generate a random permutation rand_y of the sequence seq_y using random.shuffle()
    i = num_trials
    count = 1

    while i != 0:
        # generate a random permutation rand_y of the sequence seq_y using random.shuffle()
        rand_y = list(seq_y)
        random.shuffle(rand_y)
        rand_y = ''.join(rand_y)
        #print i, rand_y
        # compute the maximum value score for the local alignment of seq_x and rand_y
        local_alignment = student.compute_local_alignment(seq_x, rand_y, PAM50, 
                                                          student.compute_alignment_matrix(seq_x, rand_y, 
                                                                                           PAM50, False))            
        if local_alignment[0] not in scoring_dictionary:
            scoring_dictionary[local_alignment[0]] = 1
        else:
            # increment the entry score in the dictionary by one
            scoring_dictionary[local_alignment[0]] += 1
        i -= 1       
   
    return scoring_dictionary

def convert_scoring_dictionary_to_list(scoring_dictionary):
    scores_list = []
    for score, count in scoring_dictionary.items():
        for i in range(count):
            scores_list.append(score)            
    return scores_list