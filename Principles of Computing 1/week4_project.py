"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level

http://www.codeskulptor.org/#user45_uEadHSRKlU_10.py
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    #sorted_hand = sorted(hand)

    #put die counts into a dictionary
    die_counts = dict()
    for die in hand:
        #print die, type(die)
        die_counts[die] = die_counts.get(die, 0) + 1

    #upper section
    max_upper_score = 0
    for die in die_counts:
        if die * die_counts[die] > max_upper_score:
            max_upper_score = die * die_counts[die]
    '''
    #lower section
    max_lower_score = 0
    if 3 in die_counts.values():
        #three_of_a_kind = True
        for die in die_counts:
            max_lower_score += die * die_counts[die]
    if 4 in die_counts.values():
        #four_of_a_kind = True
        for die in die_counts:
            max_lower_score += die * die_counts[die]
    if 5 in die_counts.values():
        #yatzee = True
        max_lower_score = 50
    if 2 in die_counts.values() and 3 in die_counts.values():
        #full_house = True
        max_lower_score = 25

    small_straight_combinations = [[1,2,3,4],[1,2,3,4,5],[1,2,3,4,6],
                                   [2,3,4,5],[2,3,4,5,6],[1,3,4,5,6],
                                   [3,4,5,6]]
    large_straight_combinations = [[1,2,3,4,5], [2,3,4,5,6]]
    if die_counts.keys() in small_straight_combinations:
        #small_straight = True
        max_lower_score = 30
    if die_counts.keys() in large_straight_combinations:
        #large_straight = True
        max_lower_score = 40

    return max(max_upper_score, max_lower_score)
    '''
    return max_upper_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    #create a tuple of outcomes
    outcome_list = []
    for number in range(num_die_sides):
        outcome_list.append(number + 1)
    outcomes = tuple(outcome_list)

    #determine expected value
    rolled_dice_enumeration = gen_all_sequences(outcomes, num_free_dice)
    count = 0
    total_score = 0
    for rolled_dice in rolled_dice_enumeration:
        new_hand = list(held_dice)[:]
        for rolled_die in rolled_dice:
            new_hand.append(rolled_die)
        count += 1
        total_score += score(new_hand)
    return total_score / float(count)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    ans = set([()])
    hand_list = list(hand)

    #the algorithm uses a binary mask to build the set of
    #potential holds. Mask value of 1 corresponds to hold
    mask = generate_mask(hand)
    for mask_tuple in mask:
        dice_to_hold = []
        mask_tuple_position = 0
        for idx in mask_tuple:
            if idx == 1:
                die_to_hold = hand_list[mask_tuple_position]
                dice_to_hold.append(die_to_hold)
            mask_tuple_position += 1
        ans.add(tuple(dice_to_hold))
    return ans

def generate_mask(hand):
    """
    This generates a binary mask of length hand. The result
    is in the form of a set
    """

    outcomes = set([0,1])	#1 is hold, 0 is not hold
    length = len(hand)
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    set_of_holds = gen_all_holds(hand)

    #need to get die values from hold_set
    #call genb all holds

    count = 0
    hold_index = dict()
    hold_scores = dict()

    for held in set_of_holds: #held is a tuple
        hold_index[count] = held
        free_dice = len(hand) - len(held)
        expected_score = expected_value(held, num_die_sides, free_dice)
        hold_scores[count] = expected_score
        count += 1
    score_list = hold_scores.values()
    max_score = max(score_list)
    for index in hold_scores.keys():
        if hold_scores.get(index) == max_score:
            index_dice_to_hold = index

    return (max_score, tuple(hold_index.get(index_dice_to_hold)))

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    #hand = (1, 1, 1, 5, 6)
    #hand = (1,2,3,4,6)
    hand = (5,5,5,2,1)
    #print score(hand)

    #gen_all_holds(hand)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score

run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
