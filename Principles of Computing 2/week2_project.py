"""
Student code for Word Wrangler game
http://www.codeskulptor.org/#user45_TXhDDQH2G7_20.py
Takes a long time to create the words
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(300)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list2 = []
    if len(list1) == 0:
        return list1

    # iterate through list1 and add anything not in list2 to list2
    for idx in range(0, len(list1)):
        if list1[idx] not in list2:
            list2.append(list1[idx])
    return list2

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list3 = []
    idx1 = 0
    idx2 = 0

    # this iterates through list1 and list2 simultaneously
    while (idx1 < len(list1)) and (idx2 < len(list2)):

        if list1[idx1] in list2:
            list3.append(list1[idx1])
            idx1 += 1
            idx2 += 1
        elif list2[idx2] in list1:
            list3.append(list2[idx2])
            idx1 += 1
            idx2 += 1
        else:
            idx1 += 1
            idx2 += 1

    return remove_duplicates(list3)

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    list3 = []
    idx1 = 0
    idx2 = 0

    while (idx1 < len(list1)) and (idx2 < len(list2)):
        if list1[idx1] < list2[idx2]:
            list3.append(list1[idx1])
            idx1 += 1
        else:
            list3.append(list2[idx2])
            idx2 += 1

    while idx1 < len(list1):
        list3.append(list1[idx1])
        idx1 += 1

    while idx2 < len(list2):
        list3.append(list2[idx2])
        idx2 += 1

    return list3

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    else:
        mid = len(list1)/2
        left = merge_sort(list1[:mid])
        right = merge_sort(list1[mid:])
        return merge(left, right)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    if len(word) < 2:
        return ['',word]

    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)

    temp_list = []
    for string in rest_strings:
        for idx in range(len(string)+1):
            string1 = string[0:int(idx)] + first + string[int(idx):]
            temp_list.append(string1)

    return merge(rest_strings, temp_list)

    #return
    #for
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    words = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        words.append(line[:-1])
    print words
    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

#list1 = ['a','b','c','d','d','e','f', 'x']
#list2 = ['g', 'h','i']

#list3 = [7,10,15]
#list4 = [10]
#list5 = [3,4,5]
#list6 = [3,4,5]
#list7 = [8,19,32,47]
#list8 = [1,5,7,8]
#list9 = [9,8,7,6]
#list10 = [2,1,1,3]
#list11 = [1]
#list12 = [2]
#list13 = [14,46,43,27,57,41,45,21,70]
#list14 = []
#list15 = [2,4,6,8]
#print merge(list14, list14)


#print intersect(list3, list4)
#print intersect(list5, list5)
#print intersect(list7, list8)

#print remove_duplicates(intersect(list1, list2))

#print merge_sort(list15)
#word1 = ""
#print word1[0:0] + 'ZZZ' + word1[0:]

#word2 = "aab"
#print gen_all_strings(word2)
