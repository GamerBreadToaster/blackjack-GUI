import os
import random
import time

global money, bet
money = 1000
card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck_blueprint = [(card, category) for category in card_categories for card in cards_list]
min_bet = 100
max_bet = 200
max_bet_money = False

# clears screen when needed. Makes the program so much nicer
def clear():
    if os.name == 'nt':
        # For Windows
        os.system('cls')
    else:
        # For Linux/macOS and IDEs (no TERM variable needed)
        os.system('clear')

def enter():
    input("press enter to continue")

# calculates score and adjusting score of aces when total score over 21. Made by AI, not me.
def calculate_score(cards):
    # 1. Calculate the initial score (Aces = 11)
    score = sum(card_value(card) for card in cards)

    # 2. Count the number of Aces in the hand
    num_aces = sum(1 for card in cards if card[0] == 'Ace')

    # 3. Adjust the score if necessary
    # While the score is over 21 AND we still have Aces that are counted as 11 (Aces left to change)
    while score > 21 and num_aces > 0:
        # Change an Ace from 11 to 1 by subtracting 10
        score -= 10
        # Decrement the count of Aces we can still change
        num_aces -= 1
    return score


def card_value(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])

# this converts the data of the cards in normal text for viewing purposes
def convert_text(cards: list, dealer_first: bool) -> str:
    results = ""
    for card in cards:
        results += card[0] + " of " + card[1]
        if dealer_first: # if it's the first-hand, show only one of the dealers' cards.
            break
        if len(cards) != cards.index(card)+1: # Gives the cards string a comma if it isn't the last card
            results += ", "
    return results

def show_cards(player_cards, dealer_cards, dealer_first: bool):
    print(f"money: {money}$ | bet: {bet}$")
    player_score = calculate_score(player_cards)
    dealer_score = calculate_score(dealer_cards)
    print("Player cards:", convert_text(player_cards, False))
    print("Player score:", player_score)
    if dealer_first:
        print("\nDealer cards:", convert_text(dealer_cards, True) + ", unknown")
        print("Dealer score:", card_value(dealer_cards[0]), "+ ?")
    else:
        print("\nDealer cards:", convert_text(dealer_cards, False))
        print("Dealer score:", dealer_score)

while True:
    # mainloop
    while True:
        # initialize betting
        clear()
        if min_bet < 0: min_bet = 0
        try:
            if max_bet == 0: max_bet_money = True
            if max_bet_money: max_bet = money
            bet = float(input(f"Money: {money}$\n"
                              f"Min bet: {min_bet}$\n"
                              f"Max bet: {max_bet}$\n"
                              f"Input your bet:\n"))
        except Exception as err:
            print("Input must be a number!")
            print(err)
            enter()
            continue
        if bet < min_bet:
            print(f"You should bet at least {min_bet}$")
            enter()
            continue
        if bet == 0:
            print("You have to bet at least more than 0$!")
            enter()
            continue
        if bet > max_bet:
            print(f"You cannot bet more than {max_bet}$")
            enter()
            continue
        else:
            money = money - bet
            break
        # end betting loop

    # initialize cards
    deck = deck_blueprint.copy()
    random.shuffle(deck)
    P_cards = []
    D_cards = []
    for _ in range(2):
        P_cards.append(deck.pop()) # player cards
        D_cards.append(deck.pop()) # dealer cards
    P_score = calculate_score(P_cards)
    D_score = calculate_score(D_cards)

    while P_score <= 21:
        clear()
        show_cards(P_cards, D_cards, True)
        P_score = calculate_score(P_cards)
        if P_score == 21 and len(P_cards) == 2: # if the player or dealer has blackjack
            choice = "s"
            time.sleep(1)
        elif D_score == 21:
            choice = "s"
            time.sleep(1)
        else:
            if len(P_cards) == 2:
                choice = input("(H)it, (S)tand, (D)ouble:\n").lower()
            else:
                choice = input("(H)it, (S)tand:\n").lower()
        if choice == "h":
            P_cards.append(deck.pop())
            P_score = calculate_score(P_cards)
            continue
        elif choice == "s":
            break
        elif choice == "d":
            if money < bet:
                print("You don't have enough money to double down!")
                continue
            money -= bet
            bet *= 2
            P_cards.append(deck.pop())
            break

    if P_score > 21:
        clear()
        show_cards(P_cards, D_cards, False)
        print("You are bust!")
        enter()
        continue
        
    P_score = calculate_score(P_cards)
    D_score = calculate_score(D_cards)
    P_amount = len(P_cards)
    D_amount = len(D_cards)

    # initial checking of blackjacks
    if P_score == 21 or D_score == 21:
        clear()
        if D_score == 21 and P_score == 21:
            show_cards(P_cards, D_cards, False)
            print("It's a push!")
            money = money + bet
            enter()
            continue
        elif D_score == 21:
            show_cards(P_cards, D_cards, False)
            print("Dealer has blackjack!!")
            enter()
            continue
        elif P_score == 21 and P_amount == 2:
            show_cards(P_cards, D_cards, False)
            print("You have a blackjack!")
            money = money + bet * 2.5
            enter()
            continue

    # populate dealer deck
    while D_score < 17:
        clear()
        show_cards(P_cards, D_cards, False)
        time.sleep(1)
        D_cards.append(deck.pop())
        D_score = calculate_score(D_cards)

    clear()
    show_cards(P_cards, D_cards, False)
    time.sleep(1)

    # results
    if D_score > 21:
        print("Dealer is bust!")
        money = money + bet * 2
        enter()
        continue
    if P_score > D_score:
        print("You win!")
        money = money + bet * 2
    elif P_score < D_score:
        print("You lose!")
    else:
        print("It's a push!")
        money = money + bet
    enter()