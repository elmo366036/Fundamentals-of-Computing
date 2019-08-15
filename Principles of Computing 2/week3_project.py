"""
Mini-max Tic-Tac-Toe Player
http://www.codeskulptor.org/#user45_xsrsWcFUjK_18.py
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60) #increase if needed

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #(score, move)
    #return (-1, -1) if game is over

    #print statements

    #print
    #print "+-----Top of Method--+"
    #print "init player", player
    #print board
    #if board.check_win() in SCORES:
    #    print "winner",board.check_win(),SCORES[board.check_win()]
    #print "+--------------------+"
    #print


    if board.check_win() in SCORES:
        return SCORES[board.check_win()], (-2,-2)

    #if board.check_win() == provided.DRAW:
    #    return 0, (-1,-1)
    #if board.check_win() == provided.PLAYERX:
    #    return 1, (-1,-1)
    #if board.check_win() == provided.PLAYERO:
    #    return -1, (-1,-1)

    potential_moves = board.get_empty_squares()
    if len(potential_moves) == board.get_dim()**2:
        return SCORES[player], (0,0)

    score_list = []
    for potential_move in potential_moves:
        board_clone = board.clone()

        #print statments
        #print
        #print "+----Potential Move--+"
        #print "POTENTIAL_move", potential_move, "by player",player

        #Move
        board_clone.move(potential_move[0], potential_move[1], player)
        #print board_clone
        #print "+--------------------+"
        #print

        #RECURSE
        #player = provided.switch_player(player)
        move = mm_move(board_clone, provided.switch_player(player))

        #print
        #print "+----POST RECURSE----+"
        #print player, score, potential_move
        #print "+--------------------+"

        #CHECK WIN
        #print "+----Winning Move----+"
        if move[0] == SCORES[player]:
            #print score, potential_move, player, provided.PLAYERX
            return move[0], potential_move
        #print "+--------------------+"

        #APPEND NON-WINNING MOVE TO LIST
        #print "+--Non-Winning Move--+"
        score_list.append((move[0], potential_move))
        #print score_list
        #print "+--------------------+"

    #EVALUATE NON_WINNING MOVE LIST
    #search for score 0 and return it
    #print "FINAL SCORE_LIST",score_list
    for potential_move in score_list:
        if potential_move[0] == 0:
            return potential_move

    return 0, (-1, -1)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """

    #don't update
    move = mm_move(board, player)

    print "move", move

    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.
# don't use x as first player


#provided.play_game(move_wrapper, 1, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


# don't test with empty board
# x = 1 (max); o = -1 (min)

#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERO, provided.PLAYERX], [provided.PLAYERX, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERO)
#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERO, provided.PLAYERX], [provided.PLAYERX, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX)

#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.PLAYERX, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERO)
#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.PLAYERX, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX)

print mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX)

#print mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX)
#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX)
