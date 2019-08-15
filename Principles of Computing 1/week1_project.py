"""
Merge function for 2048 game.
"""

def merge(line):
    '''
    Function that merges a single row or column in 2048.
    '''
    output = line[:]
    pos = 0
    zereos_added = 0
    while (pos + zereos_added) < len(line) - 1:
        frame = output[pos:pos + 2]
        #print frame
        #print output, pos, zereos_added
        if 0 in frame:
            output = shift_left(output, output.index(0))[:]
            zereos_added += 1
            continue
        elif frame[0] == frame[1]:
            output[pos] *= 2
            output = shift_left(output, pos + 1)[:]
            zereos_added += 1
            pos += 1
        else:
            pos += 1
    return output

def shift_left(list_to_shift, pos):
    '''
    This shifts the list to the right and adds a zero at the end
    '''
    list_to_shift.pop(pos)
    list_to_shift.append(0)
    #print list, index
    return list_to_shift

def test():
    '''
    This is the tester
    '''
    for _dummy_i in range(5):
        pass

    input_1 = [2,0,2,4]
    print input_1
    print merge(input_1)
    print

    input_2 = [0,0,2,2]
    print input_2
    print merge(input_2)
    print

    input_3 = [2,2,0,0]
    print input_3
    print merge(input_3)
    print

    input_4 = [2,2,2,2, 2]
    print input_4
    print merge(input_4)
    print

    input_5 = [8,16,16,8]
    print input_5
    print merge(input_5)

test()
