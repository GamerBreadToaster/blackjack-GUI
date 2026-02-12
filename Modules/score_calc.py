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