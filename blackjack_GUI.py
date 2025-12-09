import tkinter as tk
import random
from modules.players import *
from modules.image_adjuster import get_image
from modules.info_getter import get_info, set_info

# variables
screen_size = {"width" : 500, "height" : 800}
card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck_blueprint = [(card, category) for category in card_categories for card in cards_list]

# def's
def add_card(card, frame):
    if not card == "joker":
        image = get_image(card[0], card[1])
    else:
        # joker is a placeholder name for an empty card
        image = get_image("joker", "joker")
    card_label = tk.Label(frame, image=image)
    card_label.image = image
    card_amount = len(frame.winfo_children())
    if card_amount > 4:
        if not screen_size['width'] > card_amount * 125:
            screen_size['width'] = card_amount * 125
        root.geometry(f"{screen_size['width']}x{screen_size['height']}")
        root.update()
    card_label.pack(side="left", padx=10)

def clear_cards(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def clear_buttons():
    try:
        hit_button.destroy()
        stand_button.destroy()
        double_button.destroy()
    except Exception:
        pass # tries to destroy the button when it's not there is I just skip it
    root.unbind("s")
    root.unbind("h")
    root.unbind("d")
    root.unbind("<space>")
    root.unbind("<F1>")
    root.unbind("<F2>")
    root.unbind("<F3>")

def reset():
    # resets the game back to the betting fase
    global bet_input
    clear_cards(player.frame)
    clear_cards(dealer.frame)
    player.double = False
    result_button.destroy()
    root.unbind("<Return>")
    root.unbind("<F4>")
    set_info(player, settings)

    # labels and buttons
    result_label.config(text="")
    dealer_score_label.config(text="Dealer Score:")
    player_score_label.config(text="Player Score:")
    money_label.config(text=f"Cash: ${player.get_money()}")
    profit_label.config(text=f"Profit: ${player.get_profit()}")
    bet_label = tk.Label(controls_frame, text="$")
    bet_input = tk.Entry(controls_frame, width=10)
    bet_button = tk.Button(controls_frame, text="Bet\nF4", command=get_bet)
    if player.get_money() == 0:
        free_money_button = tk.Button(root, text="Use your credit card: $1000", command=lambda: give_money(free_money_button))
        free_money_button.pack()

    # bets
    bet_label.pack(side="left")
    bet_input.pack(side="left")
    bet_button.pack(side="left")
    bet_input.bind("<Return>", get_bet)
    bet_input.bind("<F4>", get_bet)
    bet_input.insert(0, f"{player.original_bet}")
    bet_input.focus_set()
    bet_input.selection_range(0, tk.END)

def game_over():
    # resetting screen to prevent any more button hitting
    global result_button
    clear_buttons()
    # buttons will already be destroyed at stand()
    result_button = tk.Button(result_frame, text="continue\nF4", command=reset)
    root.bind("<Return>", lambda event: reset())
    root.bind("<F4>", lambda event: reset())
    result_button.pack()

def sync_cards(dealers_first: bool = False):
    clear_cards(player.frame)
    clear_cards(dealer.frame)
    if dealers_first:
        add_card(dealer.cards[0], dealer.frame)
        add_card("joker", dealer.frame)
    else:
        for card in dealer.cards:
            add_card(card, dealer.frame)
    for card in player.cards:
        add_card(card, player.frame)
    dealer_score_label.config(text=f"Dealer Score: {dealer.get_score(dealers_first)}")
    player_score_label.config(text=f"Player Score: {player.get_score()}")
    money_label.config(text=f"Cash: ${player.get_money()}")
    profit_label.config(text=f"Profit: ${player.get_profit()}")

def hit():
    try:double_button.destroy()
    except Exception: pass
    root.unbind("d")
    if player.get_score() <= 21:
        player.cards.append(deck.pop())
        sync_cards(True)
    # check for 21 and higher after grabbing cards
    if player.get_score() == 21:
        stand()
    if player.get_score() > 21:
        sync_cards(False)
        check_scores()

def double():
    clear_buttons()
    player.adjust_money(-player.bet)
    player.bet = player.bet*2
    player.cards.append(deck.pop())
    player.double = True
    sync_cards(True)
    root.after(settings.cooldown, stand)

def check_scores():
    if player.get_score() > 21:
        print("score over 21")
        result_label.config(text="You are bust! You lose!")
    elif dealer.get_score() > 21:
        print("dealer score over 21")
        result_label.config(text=f"Dealers bust! You win ${player.bet*2}!")
        player.adjust_money(player.bet*2)
    elif player.get_score() == dealer.get_score():
        print("push")
        result_label.config(text="Push! You get your money back!")
        player.adjust_money(player.bet)
    elif player.get_score() > dealer.get_score():
        print("score is higher")
        result_label.config(text=f"Your score is higher! You win ${player.bet*2}!")
        player.adjust_money(player.bet*2)
    elif player.get_score() < dealer.get_score():
        print("score is lower")
        result_label.config(text="Your score is lower! You lose!")
    game_over()

def dealer_hitting():
    if dealer.get_score() >= 17:
        check_scores()
        return
    dealer.cards.append(deck.pop())
    sync_cards()
    root.after(settings.cooldown, dealer_hitting)

def stand():
    clear_buttons()
    sync_cards() # reveals the second card of dealer

    # need to use this to slowly reveal the dealers' cards. time.sleep won't work.
    root.after(settings.cooldown, dealer_hitting)

# made by AI, was lazy, this is a clean fix for blackjack
def check_blackjacks():
    player_score = player.get_score()
    dealer_score = dealer.get_score()

    player_has_bj = player_score == 21
    dealer_has_bj = dealer_score == 21

    if not player_has_bj and not dealer_has_bj:
        return

    # --- Someone has Blackjack ---

    # 1. Clean up buttons immediately
    clear_buttons()

    # 2. Schedule the reveal AND the resolution
    # We delay the entire sequence of events by 1 second (1000 ms)
    root.after(settings.cooldown, lambda: finish_blackjack_round(player_has_bj, dealer_has_bj))

def finish_blackjack_round(player_has_bj, dealer_has_bj):
    # This function runs 1 second later

    # A. Reveal the card first
    sync_cards(dealers_first=False)

    # B. THEN calculate wins/losses
    if player_has_bj and dealer_has_bj:
        result_label.config(text="Both have Blackjack! Push!")
        print("blackjack push")
        player.adjust_money(player.bet)

    elif player_has_bj:
        win_amount = player.bet + (player.bet * 1.5)
        result_label.config(text=f"Blackjack! You win ${int(win_amount)}!")
        print("player blackjack")
        player.adjust_money(win_amount)

    elif dealer_has_bj:
        result_label.config(text="Dealer has Blackjack! You lose!")
        print("dealer blackjack")

    # C. Trigger Game Over
    game_over()

def give_money(button: tk.Button):
    player.set_money(1000)
    button.destroy()
    money_label.config(text="Cash: $1000")

def start_game():
    global deck, hit_button, stand_button, double_button
    # clear cards and reset screen size
    clear_cards(player.frame)
    clear_cards(dealer.frame)
    clear_cards(controls_frame)

    hit_button = tk.Button(controls_frame, text="Hit\nF3", command=lambda: hit())
    stand_button = tk.Button(controls_frame, text="Stand\nF1", command=lambda: stand())
    if player.get_money() >= player.bet:
        double_button = tk.Button(controls_frame, text="Double\nF2", command=double)
        double_button.pack()
        root.bind('d', lambda event: double())
        root.bind('<F2>', lambda event: double())
    hit_button.pack(side="right")
    stand_button.pack(side="left")

    root.bind('h', lambda event: hit())
    root.bind('<F3>', lambda event: hit())
    root.bind('s', lambda event: stand())
    root.bind('<space>', lambda event: stand())
    root.bind('<F1>', lambda event: stand())
    screen_size['width'] = 500
    root.geometry(f"{screen_size['width']}x{screen_size['height']}")
    root.update()

    # reset deck and cards and deal cards
    deck = deck_blueprint.copy() * 6 # variable numbers of decks
    random.shuffle(deck)
    dealer.cards = []
    player.cards = []
    for _ in range(2):
        player.cards.append(deck.pop())
        dealer.cards.append(deck.pop())
    sync_cards(True)
    check_blackjacks()

def get_bet(event = None):
    try:
        player.bet = int(bet_input.get())
    except Exception as err:
        result_label.config(text = f"{err}")
        return
    if player.bet > player.get_money():
        result_label.config(text = "Can't bet more than you have!")
        return
    if player.bet <= 0:
        result_label.config(text = "Can't bet nothing or less than nothing!")
        return
    player.original_bet = player.bet
    root.unbind("<Return>")
    root.unbind("<F4>")
    player.adjust_money(-player.bet)
    set_info(player, settings)
    result_label.config(text="") # remove error text if needed
    start_game()

deck = []
dealer = Dealer()
data = get_info()
player = Player(data["money"], data["profit"])
settings = Settings(data["cooldown"])

# root
root = tk.Tk()
root.title("Blackjack")
root.geometry(f"{screen_size['width']}x{screen_size['height']}")

# frames
dealer.frame = tk.Frame(root, bg="green", pady=20)
dealer.frame.pack(side="top", fill="x")
dealer_score_label = tk.Label(root, name="dealer_score", text="Dealer Score:", bg="green")
dealer_score_label.pack()

player.frame = tk.Frame(root, bg="red", pady=20)
player.frame.pack(side="top", fill="x")
player_score_label = tk.Label(root, name="player_score", text="Player Score:", bg="red")
player_score_label.pack()

controls_frame = tk.Frame(root, pady=20)
controls_frame.pack(fill="x")

result_frame = tk.Frame(root)
result_frame.pack()
result_label = tk.Label(result_frame, text="", name="result_label")
result_label.pack(side="top")
result_button = tk.Button(result_frame, text="continue")
result_button.pack()


# money frame
money_frame = tk.Frame(root)
money_frame.pack(side="bottom")
money_label = tk.Label(money_frame, text=f"Cash: ${player.get_money()}")
profit_label = tk.Label(money_frame, text=f"Profit: ${player.get_profit()}")
profit_label.pack(side="bottom")
money_label.pack(side="bottom")

reset() # deleted duplicate code

root.mainloop()