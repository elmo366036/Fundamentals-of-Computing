# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user45_CMckK6LnAi_7.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
score = 0
wins = 0
losses = 0
timer = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

deck = []
player = []
dealer = []
player_busted = False
dealer_busted = False
dealer_wins = False
player_wins = False
player_quits = False

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        ans = "Hand contains"
        for card in self.hand:
            ans += " " + str(card)
        return ans

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        aces = 0
        for card in self.hand:
            rank = card.get_rank()
            if rank == "A":
                aces += 1
            card_value = VALUES[rank]
            hand_value += card_value
        if aces == 0:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value

    def draw(self, canvas, pos):
        ho = 10 #horizontal offset
        for card in self.hand:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.rank),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE,
                              [pos[0] + CARD_CENTER[0] + ho, pos[1] + CARD_CENTER[1]],
                              CARD_SIZE)
            ho += CARD_SIZE[0]


# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for j in range(4):
            for i in range(13):
                card = Card(SUITS[j], RANKS[i])
                self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        ans = "Deck contains"
        for card in self.deck:
            ans += " " + str(card)
        return ans


#define event handlers for buttons
def deal():
    print
    global in_play, deck, player, dealer, dealer_busted, player_busted, player_quits, losses, dealer_wins, player_wins

    if in_play:
        player_quits = True
        losses += 1
        #print "you quit!"

    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    for i in range(2):
        card = deck.deal_card()
        player.add_card(card)
        card = deck.deal_card()
        dealer.add_card(card)
    in_play = True
    dealer_busted = False
    player_busted = False
    dealer_wins = False
    player_wins = False

    #print "Player " + str(player) + "   Value is " + str(player.get_value())
    #print "Dealer " + str(dealer) + "   Value is " + str(dealer.get_value())

def hit():
    global in_play, deck, player, losses, player_busted, dealer_wins, player_quits

    if player_busted or not in_play:
        return
    player_quits = False
    card = deck.deal_card()
    card_value = VALUES[card.get_rank()]
    player.add_card(card)
    hand_value = player.get_value()

    #print "Player " + str(player) + "   Value is " + str(player.get_value())

    if hand_value > 21:
        #print "You have busted"
        in_play = False
        player_busted = True
        dealer_wins = True
        losses += 1
        #print "Dealer Wins!!!"


def stand():
    global deck, dealer, losses, wins, dealer_busted, player_busted, in_play, player_wins, dealer_wins

    if player_busted or dealer_wins or player_wins
        return
    in_play = False
    player_quits = False
    hand_value = dealer.get_value()
    while hand_value < 17:
        card = deck.deal_card()
        card_value = VALUES[card.get_rank()]
        dealer.add_card(card)
        hand_value = dealer.get_value()

        #print "Dealer " + str(dealer) + "   Value is " + str(dealer.get_value())

        if hand_value > 21:
            #print "Dealer has busted"
            dealer_busted = True
            player_wins = True
            dealer_wins = False
            break

    if (dealer.get_value() >= player.get_value() and not dealer_busted) or player_busted:
        losses += 1
        dealer_wins = True
        player_wins = False
        #print "Dealer Wins!!!"
    else:
        wins += 1
        dealer_wins = False
        player_wins = True
        #print "You Win!"

# draw handler
def draw(canvas):
    global player_quits, timer, in_play
    canvas.draw_text("Blackjack",(100,50), 60 ,"Black", "serif")

    player.draw(canvas, [0, 150])
    dealer.draw(canvas, [0, 350])

    if player_quits:
        canvas.draw_text("Player Quits, Dealer Wins",(100, 312), 40, "Red")
        timer += 1
        if timer > 60: #this makes the message display for about a second
            player_quits = False
            timer = 0

    if in_play:
        ho = 10 #horizontal offset
        card_back_loc = (CARD_BACK_CENTER[0],
                        CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE,
                          [0 + CARD_BACK_CENTER[0] + ho, 350 + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)
        canvas.draw_text("Hit or Stand?",(10, 140), 40, "White")
        if dealer_wins:
            canvas.draw_text("Dealer Wins",(100, 312), 40, "Red")
            #print "dealer wins in play"

    else:
        canvas.draw_text("New Deal?",(10, 140), 40, "White")
        if dealer_wins:
            canvas.draw_text("Dealer Wins",(100, 312), 40, "Red")
            #print "dealer wins not in play"
        if player_wins:
            canvas.draw_text("Player Wins",(100, 312), 40, "White")

    canvas.draw_text("Player Score " + str(wins), (10, 500), 30, "Blue")
    canvas.draw_text("Dealer Score " + str(losses), (10, 540), 30, "Blue")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
