"""
Monte Carlo Tic-Tac-Toe Player
http://www.codeskulptor.org/#user45_SywA2gH8Ce_8.py
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 250     	# Number of trials to run. 250 seems to work well
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
BOARD_DIMENSIONS = 3

# Add your functions here.
# mc stands for MaChine

def mc_trial(board, player):
    '''
    Simulates a game with monte carlo using a board
    starting with the next player to move. This simply alternates the random
    placement of Xs and O until the game ends with a winner or a draw
    '''
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        random_choice = random.choice(empty_squares)
        board.move(random_choice[0], random_choice[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    '''
    This calculates the score of each grid spot after a win. Player is the
    machine player. If the machine wins, use SCORE_CURRENT, else, use SCORE_OTHER.
    If there is a draw it simply returns.
    '''

    winner = board.check_win()

    #determine who won and what to set score to or if it was a draw
    if winner == provided.DRAW:
        return
    elif winner == player:
        score = SCORE_CURRENT
    else:
        score = SCORE_OTHER

    #calculate the score of the board for player (the machine)
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            current_square = board.square(row, col)
            if current_square != provided.EMPTY:
                if current_square == winner:
                    scores[row][col] += score
                else:
                    scores[row][col] -= score

def get_best_move(board, scores):
    '''
    Pick the best move based on the monte carlo generated score and return it
    '''
    max_score = float('-Inf')	#if ntrials = 1 then this cannot be 0
    free_space = board.get_empty_squares()
    selected_square_list = []

    #iterate over score and build a list of potential squares that are empty and
    #have the highest score
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            #if the score for a potential move is equal to or greater than
            #current max score and that spot has not yet been used, add it to
            #a list
            selected_square = (row, col)
            if scores[row][col] > max_score and (row, col) in free_space:
                max_score = scores[row][col]
                selected_square_list = [] #clear out the list if there is a new max_score
                selected_square_list.append(selected_square)
            elif scores[row][col] == max_score and (row, col) in free_space:
                selected_square_list.append(selected_square)

    #select a random spot from the list
    return random.choice(selected_square_list)

def mc_move(board, player, trials):
    '''
    This is the function for the machine player
    '''
    #initalize some variables
    games_played = 0
    game_scores = []

    #initialize game_scores to 0
    while len(game_scores) < board.get_dim():
        game_scores.append([0]*board.get_dim())

    #this runs the monte carlo simulation. It clones the board,
    #simulates a game, and then scores the result of the game.
    #it does this trials number of times
    while games_played < trials:
        cloned_board = board.clone()
        mc_trial(cloned_board, player)
        mc_update_scores(game_scores, cloned_board, player)
        games_played += 1

    #this calls get best move and returns it. The best move is based on
    #game_scores
    return get_best_move(board, game_scores)

# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.


#console based. this will allow the game to play itself and prints the result to the right
provided.play_game(mc_move, NTRIALS, False)

#gui. this will create a gui for the player to play against the machine
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
