'''
   project 4
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


def copy_dictionary(in_dict):
    '''perform deep copy of a dictionary of dictionaries'''
    copy_dict = {}

    for key_a, value_a in in_dict.items():
        temp = {}
        for key_b, value_b in value_a.items():
            if value_b >= 0:
                temp[key_b] = value_b
            else:
                temp[key_b] = 0
        copy_dict[key_a] = temp
        
    return copy_dict

#print copy_dictionary(build_scoring_matrix("atcg", 10, 4, -4))    

#print build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)

#print compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True)     
#print compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, False)

#print compute_global_alignment('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0]])
#print compute_global_alignment('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0, -4], [-4, 6]])
#print compute_global_alignment('ATG', 'ACG', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0, -4, -8, -12], [-4, 6, 2, -2], [-8, 2, 8, 4], [-12, -2, 4, 14]])
#print compute_global_alignment('firetruck', 'freck', {'-': {'-': 0, 'a': 0, 'c': 0, 'b': 0, 'e': 0, 'd': 0, 'g': 0, 'f': 0, 'i': 0, 'h': 0, 'k': 0, 'j': 0, 'm': 0, 'l': 0, 'o': 0, 'n': 0, 'q': 0, 'p': 0, 's': 0, 'r': 0, 'u': 0, 't': 0, 'w': 0, 'v': 0, 'y': 0, 'x': 0, 'z': 0}, 'a': {'-': 0, 'a': 2, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'c': {'-': 0, 'a': 1, 'c': 2, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'b': {'-': 0, 'a': 1, 'c': 1, 'b': 2, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'e': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 2, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'd': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 2, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'g': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 2, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'f': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 2, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'i': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 2, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'h': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 2, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'k': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 2, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'j': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 2, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'm': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 2, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'l': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 2, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'o': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 2, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'n': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 2, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'q': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 2, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'p': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 2, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 's': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 2, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'r': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 2, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'u': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 2, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 't': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 2, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'w': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 2, 'v': 1, 'y': 1, 'x': 1, 'z': 1}, 'v': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 2, 'y': 1, 'x': 1, 'z': 1}, 'y': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 2, 'x': 1, 'z': 1}, 'x': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 2, 'z': 1}, 'z': {'-': 0, 'a': 1, 'c': 1, 'b': 1, 'e': 1, 'd': 1, 'g': 1, 'f': 1, 'i': 1, 'h': 1, 'k': 1, 'j': 1, 'm': 1, 'l': 1, 'o': 1, 'n': 1, 'q': 1, 'p': 1, 's': 1, 'r': 1, 'u': 1, 't': 1, 'w': 1, 'v': 1, 'y': 1, 'x': 1, 'z': 2}}, [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 3, 3, 3], [0, 2, 4, 4, 4, 4], [0, 2, 4, 6, 6, 6], [0, 2, 4, 6, 7, 7], [0, 2, 4, 6, 7, 8], [0, 2, 4, 6, 7, 8], [0, 2, 4, 6, 8, 8], [0, 2, 4, 6, 8, 10]])  

#print compute_local_alignment('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0]])     
#print compute_local_alignment('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0, 0], [0, 6]]) 




