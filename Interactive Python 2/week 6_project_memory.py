# implementation of card game - Memory
# http://www.codeskulptor.org/#user45_LifVkPz3B7_0.py

import simplegui
import random

CARD_WIDTH = 50
CARD_HEIGHT = 100
CARD_BORDER = 5
NUM_CARDS = 16
cards = []
card_selected = []
card_selection_count = 0
card_matched = []
temp = [0,0] #used for comparing selected cards [value, index]
turns = 0

# helper function to initialize globals
def new_game():
    reset_all_lists()
    cards = shuffle_cards() #create random cards

def shuffle_cards():
    for count in range(1, NUM_CARDS + 1):
        card_selected.append(False)
        card_matched.append(False)
        if count <= NUM_CARDS/2:
            cards.append(count)
        else:
            cards.append(count - NUM_CARDS/2)
    random.shuffle(cards)

def reset_selection_tracker():
    global card_selection_count
    card_selection_count = 0
    for count in range(0, NUM_CARDS):
        card_selected[count] = False

def reset_all_lists():
    global cards, card_selected, card_selection_count, card_matched, temp, turns
    cards = []
    card_selected = []
    card_selection_count = 0
    card_matched = []
    temp = [0,0]
    turns = 0

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global card_selection_count, temp, turns
    card = pos[0] / CARD_WIDTH
    if card_selected[card] == True: #ignore already selected card
        return
    card_selection_count += 1
    card_selected[card] = True
    if card_selection_count > 2:
        reset_selection_tracker()
        card_selected[card] = True
        card_selection_count = 1
    if card_selection_count == 2:
        turns += 1
        if temp[0] == cards[card]:
            card_matched[temp[1]] = True
            card_matched[card] = True
            reset_selection_tracker()
    if card_selection_count == 1:
        temp[0] = cards[card] 	#value of card
        temp[1] = card			#index of card

# cards are logically 50x100 pixels in size
def draw(canvas):
    for card_number in range (1, NUM_CARDS+1):
        x = 1 + (card_number - 1)*CARD_WIDTH
        if card_selected[card_number - 1] == False and card_matched[card_number - 1] == False:
            canvas.draw_polygon([(x,1),
                             (x,CARD_HEIGHT),
                             (x+CARD_WIDTH,CARD_HEIGHT),
                             (x+CARD_WIDTH,1)],
                            CARD_BORDER, "Brown", "Green")
        elif card_selected[card_number - 1] == True:
            canvas.draw_polygon([(x,1),
                             (x,CARD_HEIGHT),
                             (x+CARD_WIDTH,CARD_HEIGHT),
                             (x+CARD_WIDTH,1)],
                            CARD_BORDER, "Brown", "Black")
            canvas.draw_text(str(cards[card_number - 1]),
                         [(x + CARD_WIDTH/2 - 1.5*CARD_BORDER),
                          (CARD_HEIGHT/2 + CARD_BORDER)],
                         25, "White")
        elif card_matched[card_number - 1] == True:
            canvas.draw_polygon([(x,1),
                             (x,CARD_HEIGHT),
                             (x+CARD_WIDTH,CARD_HEIGHT),
                             (x+CARD_WIDTH,1)],
                            CARD_BORDER, "Brown", "Blue")
            canvas.draw_text(str(cards[card_number - 1]),
                         [(x + CARD_WIDTH/2 - 1.5*CARD_BORDER),
                          (CARD_HEIGHT/2 + CARD_BORDER)],
                         25, "White")
    label.set_text("Turns = " + str(turns))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 801, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
