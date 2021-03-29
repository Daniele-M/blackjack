import random
import time

class Card(object):

    def __init__(self, suit, card, value):
        #Spade, Hearts...
        self.suit = suit
        #Ace, 1, 2, King...
        self.card = card
        #Value of the card, King -> 10...
        self.value = value


suits = ["Spades", "Hearts", "Clubs", "Diamonds"]

#How suits will be represented
suits_value = {"Spades": "S", "Hearts": "H", "Clubs": "C", "Diamonds": "D"}

cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

cards_value = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

#Initialize the deck
deck = []
#Initialize the hands
player_hand = []
dealer_hand = []
#Initialize hands for the split
player_split = []
dealer_split = []
#Initialize the money and the bet.
money = [500, 0]

#Populate the deck
for i in range(0,2):
    for suit in suits:
        for card in cards:
            deck.append(Card(suits_value[suit], card, cards_value[card]))

# for i in range(0, 104):
#     print(f"{deck[i].card}{deck[i].suit}")
# for i in range(0, 104):
#     print(deck[i].__dict__)


# Gets the bet for a minimum of 10
def place_bet():
    over_balance = True
    print(f"Your balance : \t{money[0]}")
    while over_balance:
        try:
            money[1] = int(input("Place your bet.\n> "))
            if money[1] > money[0]:
                print("You don't have enough money.")
            if money[1] <= 10:
                print("You must bet at least 10 coins.")
            else:
                over_balance = False
        except ValueError:
            print("Please enter a valid ammount.\n")

    print(f"You bet {money[1]} coins.\n")


# Also allows to surrender
def check_split_doubledown_insurance():
    possible_moves = []

    # Check if split is possible
    if player_hand[0].value == player_hand[1].value:
        possible_moves.append("split")
    # Check if double down is possible
    if score(player_hand) >= 9 and score(player_hand) <= 11:
        possible_moves.append("doubledown")
    # Check if insurance is possible
    if dealer_hand[0].value == 11:
        possible_moves.append("insurance")


    print("You can:  surrender  keep playing  ", end=" ")
    for i in possible_moves:
        print(f"{i}", end=" ")
    print("\nType 0 if you want to go to the drawing phase.")
    possible_moves.append("0")
    possible_moves.append("surrender")

    while True:
        choice = input("> ")
        if choice in possible_moves:
            if choice == "0":
                return
            elif choice == "split":
                if money[1] * 2 > money[0]:
                    print("You don't have enouh money for this.")
                else:
                    split()
            elif choice == "doubledown":
                if money[1] * 2 > money[0]:
                    print("You don't have enouh money for this.")
                else:
                    double_down()
            elif choice == "insurance":
                if money[1]/2 + money[1] > money[0]:
                    print("You don't have enouh money for this.")
                else:
                    insurance()
            elif choice == "surrender":
                surrender()
            else:
                print("I didn't undestand, please try again\n")


def surrender():

    print("\nYou decided to surrender.")
    print("You will lose half of what you bet.\n")
    money[1] /= 2
    end_game("dealer")

# The draw_hand function modified to word for the split function
# It returns the bet for each hand after splitting, positive for wins, negatives for losses, null for ties.
def draw_hand_split(player_list, dealer_list):

    show_hand(player_list)
    show_hand(dealer_list)

    first_bet = money[1]
    drawing = True
    while drawing:
        if score(player_list) == 21:
            drawing = False
        else:
            draw = input("Hit or stay?\n> ")
            if draw == "hit":
                player_list.append(deck.pop(0))
                show_hand(player_list)
                check_overflow(player_list)
                if score(player_list) > 21:
                    first_bet = 0 - money[1]
                    drawing = False
            elif "stay" in draw or "stand" in draw:
                drawing = False
            else:
                print("I didn't undestand.")
    if first_bet >= 0:
        while score(dealer_list) < 17:
            dealer_list.append(deck.pop(0))
            show_hand(dealer_list)
            check_overflow(dealer_list)

        if score(dealer_list) <= 21:
            if score(player_list) < score(dealer_list):
                first_bet = 0 - money[1]
            if score(player_list) == score(dealer_list):
                first_bet = 0
    else:
        print("You overflowed.\n")

    return first_bet



def split():
    print("You split your cards.\n")

    player_split.append(player_hand.pop())
    dealer_split.append(deck.pop(0))

    first_bet = draw_hand_split(player_hand, dealer_hand)
    second_bet = draw_hand_split(player_split, dealer_split)

    split_bet = first_bet + second_bet
    money[0] += split_bet

    if split_bet > 0:
        print(f"You won {split_bet} coins.\n")
    if split_bet == 0:
        print(f"You won one hand and lost the other.")
        print("You didn't lose or win anything")
    if split_bet < 0:
        print(f"You lost {-split_bet} coins.")
        if money[0] == 0:
            print("It looks like you lost all your coins.")
            print("Be more careful next time. Goodbye!")
            exit(0)

    for card in range(0, len(player_split)):
        deck.append(player_split.pop(0))
    for card in range(0, len(dealer_split)):
        deck.append(dealer_split.pop(0))

    end_game("split")



def double_down():
    print("You decided to double down, you can only drawn one more card.")
    money[1] *= 2

    loop = True
    while loop:
        choice = input("Hit or stay?\n> ")
        if choice == "hit":
            loop = False
            player_hand.append(deck.pop(0))
            show_hand(player_hand)
        elif choice == "stay":
            loop == False
        else:
            print("I didn't undestand.\n")

    if score(player_hand) > 21:
        end_game("dealer")
    else:
        draw_card("dealer")

        if score(player_hand) < score(dealer_hand):
            end_game("dealer")
        elif score(player_hand) > score(dealer_hand):
            end_game("player")
        else:
            end_game("tie")



def insurance():
    ins = money[1]/2

    draw_card("player")
    draw_card("dealer")

    if score(dealer_hand) == 21:
        print("The dealer scored 21 but you have an insurance.")
        print("Nothing was lost this turn.")
        end_game("insurance")
    elif score(player_hand) < score(dealer_hand):
        money[1] += ins
        end_game("dealer")
    else:
        money[1] -= ins
        end_game("player")



def blackjack():
    if score(player_hand) == 21:
        while score(dealer_hand) < 17:
            dealer_hand.append(deck.pop(0))
            show_hand(dealer_hand)
            check_overflow(dealer_hand)
        if score(dealer_hand) == 21:
            end_game("tie")
        else:
            print("You got a Blackjack!\nYou will gain 3/2 of what you bet.")
            money[1] *= 1.5
            end_game("player")




#End the game updating the balance and asking for a new game
def end_game(winner):

    if winner == "tie":
        print("It's a tie!\n")
    elif winner == "player":
        print("You won the game!\n")
        money[0] += money[1]
        print(f"You won {money[1]} coins.\n")
    elif winner == "dealer":
        print("The dealer won the game")
        money[0] -= money[1]
        print(f"You lost {money[1]} coins.\n")
        if money[0] == 0:
            print("It looks like you lost all your coins.")
            print("Be more careful next time. Goodbye!")
            exit(0)

    print(f"Your balance is now {money[0]} coins.\n")
    play_again = input("Do you want to keep playing?\n> ")

    if play_again == "y" or play_again == "yes":

        print("\nPreparing a new game...\n")
        for card in range(0, len(player_hand)):
            deck.append(player_hand.pop(0))
        for card in range(0, len(dealer_hand)):
            deck.append(dealer_hand.pop(0))
        core_game()

    else:
        print("See you next time!")
        exit(0)


#Checks of the value of the card exceed 21
#If true calls the end_game function with the winner
def check_overflow(hand):

    if score(hand) > 21:
        for card in hand:
            if card.value == 11:
                card.value = 1
                show_hand(hand)


#Draws cards for player and dealer
def draw_card(drawer):

    if drawer == "player":
        drawing = True

        while drawing:
            if score(player_hand) == 21:
                drawing = False
            else:
                draw = input("Hit or stay?\n> ")
                if draw == "hit":
                    player_hand.append(deck.pop(0))
                    show_hand(player_hand)
                    check_overflow(player_hand)
                    if score(player_hand) > 21:
                        end_game("dealer")
                elif "stay" in draw or "stand" in draw:
                    drawing = False
                else:
                    print("I didn't undestand.")

    else:
        while score(dealer_hand) < 17:
            dealer_hand.append(deck.pop(0))
            show_hand(dealer_hand)
            check_overflow(dealer_hand)
            if score(dealer_hand) > 21:
                end_game("player")


#Returns the score of the requested player
def score(hand):
    scores = 0
    for i in hand:
        scores += i.value
    return scores


#Prints the hand of the requested player
def show_hand(hand):
    time.sleep(0.5)
    if hand == player_hand or hand == player_split:
        score_player = score(hand)
        print("Your hand: ", end=" ")
        for i in hand:
            print(f"{i.card}{i.suit}", end=" ")
        print(f"\t\t\tTotal = {score_player}\n")
    else:
        score_dealer = score(hand)
        print("Dealer hand: ", end=" ")
        for i in hand:
            print(f"{i.card}{i.suit}", end=" ")
        print(f"\t\t\tTotal = {score_dealer}\n")
    time.sleep(0.5)


#Deals the first cards and handles the core of the game
def core_game(SHUFFLE=False):          # Shuffle only the first turn

    place_bet()

    if SHUFFLE:
        random.shuffle(deck)

    player_hand.append(deck.pop(0))
    dealer_hand.append(deck.pop(0))
    player_hand.append(deck.pop(0))

    show_hand(player_hand)
    show_hand(dealer_hand)

    # Check if the player has a blackjack
    blackjack()

    check_split_doubledown_insurance()

    draw_card("player")
    draw_card("dealer")
    # After the calls nor the player or the dealer overflowed
    # So we have to check who has the highter score

    if score(player_hand) < score(dealer_hand):
        end_game("dealer")
    elif score(player_hand) > score(dealer_hand):
        end_game("player")
    else:
        end_game("tie")

core_game(SHUFFLE=True)
