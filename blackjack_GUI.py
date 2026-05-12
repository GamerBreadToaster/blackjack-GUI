import tkinter as tk
import random
from Modules.classes import *
from Modules.image_adjuster import add_card, get_image
from Modules.file_adjuster import get_info, set_info, get_settings, add_history
from Modules.settings_GUI import settings_gui
from Modules.stats_GUI import stats_gui
from Modules.result_checking import check_scores, check_blackjack
from Modules.debug import *

# variables
screen_size = {"width" : 500, "height" : 800}
card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck_blueprint = [(card, category) for category in card_categories for card in cards_list]
game_finished = False

# def's
def clear_cards(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def clear_buttons():
    # does as it's said, clears the buttons off-screen and unbinds all hotkeys
    #TODO: change the destroying of buttons to just disabling them to prevent the try except catch fucking up unseen bugs
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
    global bet_input, settings_button, game_finished
    clear_cards(game.player.frame)
    clear_cards(game.dealer.frame)
    game.player.double = False
    result_button.destroy()
    root.unbind("<Return>")
    root.unbind("<F4>")
    game_finished = False

    # labels and buttons
    result_label.config(text="", font=("Arial", 14, "bold"), fg="red")
    dealer_score_label.config(text="Dealer Score:")
    player_score_label.config(text="Player Score:")
    money_label.config(text=f"Cash: ${game.player.get_money()}")
    profit_label.config(text=f"Profit: ${game.player.get_profit()}")
    session_profit_label.config(text=f"Session profit: ${game.player.get_profit(True)}")
    winstreak_label.config(text=f"Winstreak: {game.player.stats.get_winstreak()}")
    bet_label = tk.Label(controls_frame, text="$")
    bet_input = tk.Entry(controls_frame, width=10)
    bet_button = tk.Button(controls_frame, text="Bet\nF4", command=get_bet)
    if game.player.get_money() == 0:
        credit_card_button = tk.Button(root, text=f"Use your credit card: ${game.settings.credit_card_debt}", command=lambda: give_money(credit_card_button))
        credit_card_button.pack()

    # bets
    bet_label.pack(side="left")
    bet_input.pack(side="left")
    bet_button.pack(side="left")
    bet_input.bind("<Return>", get_bet)
    bet_input.bind("<F4>", get_bet)
    bet_input.insert(0, f"{game.player.original_bet}")
    bet_input.focus_set()
    bet_input.selection_range(0, tk.END)

    # buttons in corners
    #TODO: fix the stats button not anchored to bottom left corner
    settings_button = tk.Button(bottom_frame, text="settings", command=edit_settings)
    settings_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)
    stats_button = tk.Button(bottom_frame, text="stats", command=lambda: stats_gui())
    stats_button.place(relx=1.0, rely=1.0, anchor="sw", x=-490, y=-5)

    # reset screen
    screen_size = {"width": 500, "height": 800}
    root.geometry(f"{screen_size['width']}x{screen_size['height']}")
    root.update()

def game_over(result: Result):
    # resetting screen to prevent any more button hitting
    global result_button, game_finished
    clear_buttons()
    # buttons will already be destroyed at stand()
    result_button = tk.Button(result_frame, text="continue\nF4", command=reset)
    root.bind("<Return>", lambda event: reset())
    root.bind("<F4>", lambda event: reset())
    result_button.pack()
    set_info(game.player)
    if game.settings.record_history:
        add_history(result)
    game_finished = True

def sync_cards(dealers_first: bool = False):
    # this handles the logic of showing all cards on screen, and resizing the screen if necessary

    clear_cards(game.player.frame)
    clear_cards(game.dealer.frame)
    # if the game.player hasn't stood yet, the game.dealer won't reveal his second card
    if dealers_first:
        add_card(game.dealer.cards[0], game.dealer.frame)
        add_card("joker", game.dealer.frame)
    else:
        for card in game.dealer.cards:
            add_card(card, game.dealer.frame)
    for card in game.player.cards:
        add_card(card, game.player.frame)

    # changes the labels to reflect the current game state
    dealer_score_label.config(text=f"Dealer Score: {game.dealer.get_score(dealers_first)}")
    player_score_label.config(text=f"Player Score: {game.player.get_score()}")
    money_label.config(text=f"Cash: ${game.player.get_money()}")
    profit_label.config(text=f"Profit: ${game.player.get_profit()}")
    session_profit_label.config(text=f"Session profit: ${game.player.get_profit(True)}")
    winstreak_label.config(text=f"Winstreak: {game.player.stats.get_winstreak()}")

    # resize screen
    max_cards = max(len(game.player.frame.winfo_children()), len(game.dealer.frame.winfo_children()))
    if max_cards > 4:
        required_width = max_cards * 125
        # only resizes when necessary
        if screen_size["width"] < required_width:
            screen_size["width"] = required_width
            root.geometry(f"{screen_size["width"]}x{screen_size["height"]}")
            root.update()

def hit():
    try:double_button.destroy()
    except Exception: pass
    root.unbind("d")
    if game.player.get_score() <= game.settings.max_score:
        game.player.cards.append(game.get_card())
        sync_cards(True)
    # check for 21 and higher after grabbing Card
    if game.player.get_score() == game.settings.max_score:
        game.player.stats.hit_21 += 1
        if game.settings.stand_at_max:
            clear_buttons() # clear the keybinds so you can't stand twice
            root.after(game.settings.cooldown, lambda: stand())
    if game.player.get_score() > game.settings.max_score:
        sync_cards(False)
        final_check_scores()

def double():
    # doubling down stops your turn immediately
    clear_buttons()
    game.player.adjust_money(-game.player.bet)
    game.player.bet = game.player.bet*2
    game.player.cards.append(game.get_card())
    game.player.double = True
    game.player.stats.double_downs += 1
    sync_cards(True)
    root.after(game.settings.cooldown, stand)

def final_check_scores():
    result = check_scores(game.player, game.dealer, game.settings)
    result_label.config(text=result.get_result_string())
    log(f"round over\ngame.player cards: {game.player.cards} | player score: {game.player.get_score()}\ndealer cards: {game.dealer.cards} | dealer score: {game.dealer.get_score()}")
    match result.get_win_type():
        case ResultType.PLAYER_BUST:
            log("player bust")
            game.player.stats.player_bust += 1
            game.player.stats.total_lost += game.player.bet
            game.player.stats.adjust_winstreak(True)
        case ResultType.DEALER_BUST:
            log("dealer bust")
            game.player.adjust_money(game.player.bet * 2)
            game.player.stats.dealer_bust += 1
            game.player.stats.total_won += game.player.bet
            game.player.stats.adjust_winstreak()
        case ResultType.PUSH:
            log("push")
            game.player.adjust_money(game.player.bet)
            game.player.stats.ties += 1
        case ResultType.PLAYER_HIGHER:
            log("player has higher score than dealer")
            game.player.adjust_money(game.player.bet * 2)
            game.player.stats.higher_score += 1
            game.player.stats.total_won += game.player.bet
            game.player.stats.adjust_winstreak()
        case ResultType.DEALER_HIGHER:
            log("dealer has higher scrore than player")
            game.player.stats.lower_score += 1
            game.player.stats.total_lost += game.player.bet
            game.player.stats.adjust_winstreak(True)
    game_over(result)

def dealer_hitting():
    if game.dealer.get_score() >= game.settings.dealer_stop:
        final_check_scores()
        return
    game.dealer.cards.append(game.get_card())
    sync_cards()
    root.after(game.settings.cooldown, dealer_hitting)

def stand():
    clear_buttons()
    sync_cards() # reveals the second card of dealer

    # need to use this to slowly reveal the dealers' Cards. time.sleep won't work.
    root.after(game.settings.cooldown, dealer_hitting)

# made by AI, just checks for blackjack
def first_check_blackjacks():
    if not game.player.get_score() == 21 and not game.dealer.get_score() == 21:
        return
    # --- Someone has Blackjack ---

    # 1. Clean up buttons immediately
    clear_buttons()

    # 2. Schedule the reveal AND the resolution
    root.after(game.settings.cooldown, lambda: finish_blackjack_round())

def finish_blackjack_round():
    # This function runs 1 second later

    # A. Reveal the card first
    sync_cards(dealers_first=False)

    # B. THEN calculate wins/losses
    # made with my bare hands
    result = check_blackjack(game.player, game.dealer)
    result_label.config(text=result.get_result_string())
    log(f"round over\nplayer cards: {game.player.cards} | player score: {game.player.get_score()}\ndealer cards: {game.dealer.cards} | dealer score: {game.dealer.get_score()}")
    match result.get_win_type():
        case ResultType.PUSH_BLACKJACK:
            log("blackjack push")
            game.player.stats.blackjack_push += 1
            game.player.adjust_money(game.player.bet)
        case ResultType.PLAYER_BLACKJACK:
            log("player blackjack")
            win_amount = game.player.bet + (game.player.bet * 1.5)
            game.player.stats.won_by_blackjack += 1
            game.player.stats.adjust_winstreak()
            game.player.stats.total_won += win_amount - game.player.bet
            game.player.adjust_money(win_amount)
        case ResultType.DEALER_BLACKJACK:
            log("dealer blackjack")
            game.player.stats.total_lost += game.player.bet
            game.player.stats.lost_by_blackjack += 1
            game.player.stats.adjust_winstreak(True)

    # C. Trigger Game Over
    game_over(result)

def give_money(button: tk.Button):
    game.player.set_money(game.settings.credit_card_debt)
    game.player.stats.used_credit_card += 1
    button.destroy()
    money_label.config(text=f"Cash: ${game.settings.credit_card_debt}")

def start_game():
    global game, hit_button, stand_button, double_button
    # clear Cards and reset screen size
    clear_cards(game.player.frame)
    clear_cards(game.dealer.frame)
    clear_cards(controls_frame)
    settings_button.destroy()

    hit_button = tk.Button(controls_frame, text="Hit\nF3", command=lambda: hit())
    stand_button = tk.Button(controls_frame, text="Stand\nF1", command=lambda: stand())
    if game.player.get_money() >= game.player.bet:
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

    # game logic
    game.add_round()

    # reset deck and Cards and deal Cards
    if game.get_round() % game.settings.shuffle_after == 0:
        game.shuffle_deck()
    game.dealer.cards = []
    game.player.cards = []
    for _ in range(2):
        game.player.cards.append(game.get_card())
        game.dealer.cards.append(game.get_card())
    sync_cards(True)
    if game.settings.enable_blackjack:
        first_check_blackjacks()

def get_bet(event = None):
    try:
        game.player.bet = float(bet_input.get())
    except Exception as err:
        result_label.config(text = f"{err}")
        return
    if game.player.bet > game.player.get_money():
        result_label.config(text = "Can't bet more than you have!")
        return
    if game.player.bet <= 0.01:
        result_label.config(text = "You should bet at least 1 cent!")
        return
    game.player.original_bet = game.player.bet
    root.unbind("<Return>")
    root.unbind("<F4>")
    game.player.adjust_money(-game.player.bet)
    set_info(game.player)
    result_label.config(text="") # remove error text if needed
    start_game()

def on_close():
    if not bet_input.winfo_exists(): # if the betting button doesn't exist
        if game_finished:
            log("exiting after reset")
            reset()
        else:
            game.player.stats.total_lost += game.player.bet
            game.player.stats.player_bust += 1
            set_info(game.player)
            result = Result(game.player, game.dealer, ResultType.PLAYER_EXIT)
            if game.settings.record_history:
                add_history(result)
            log("adding loss")
    log("exiting program")
    root.destroy()

# global Game class for eventual full refactoring to class-based structure
class Game:
    def __init__(self):
        self.__deck = []
        self.__rounds_played = 0
        self.dealer = Dealer()
        data = get_info()
        data_settings = get_settings()
        stats_data = Stats(**data.get("stats", {}))
        self.player = Player(data["money"], data["profit"], stats_data)
        self.settings = Settings(**data_settings)

    def get_card(self):
        try:
            card = self.__deck.pop(0)
            return card
        except IndexError:
            log("emergency shuffle. Deck was empty")
            self.shuffle_deck()
            card = self.__deck.pop(0)
            return card
        finally:
            self.__deck.append(card)

    def add_round(self):
        self.__rounds_played += 1
        log(f"round: {self.__rounds_played}")

    def get_round(self) -> int:
        return self.__rounds_played

    def shuffle_deck(self):
        self.__deck = deck_blueprint.copy() * game.settings.deck_amount  # variable numbers of decks
        random.shuffle(self.__deck)
        log(f"shuffling deck after {self.__rounds_played} rounds played, shuffle_after settings: {game.settings.shuffle_after}, deck amount: {game.settings.deck_amount}")

game = Game()

# TODO: Wrap this in a GameTK class, instead of the Game class

class GameTK:
    def __init__(self):
    # root
        self.root = tk.Tk()
        self.root.title("Blackjack")
        self.root.geometry(f"{screen_size['width']}x{screen_size['height']}")
        self.root.protocol("WM_DELETE_WINDOW", on_close) # make sure closing the program counts as folding

        # frames
        game.dealer.frame = tk.Frame(self.root, bg="green", pady=20)
        game.dealer.frame.pack(side="top", fill="x")
        self.dealer_score_label = tk.Label(self.root, name="dealer_score", text="Dealer Score:", bg="green")
        self.dealer_score_label.pack()

        game.player.frame = tk.Frame(self.root, bg="red", pady=20)
        game.player.frame.pack(side="top", fill="x")
        self.player_score_label = tk.Label(self.root, name="player_score", text="Player Score:", bg="red")
        self.player_score_label.pack()

        self.controls_frame = tk.Frame(self.root, pady=20)
        self.controls_frame.pack(fill="x")

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack()
        self.result_label = tk.Label(self.result_frame, font=("Arial", 14, "bold"), fg="red", name="result_label")
        self.result_label.pack(side="top")
        self.result_button = tk.Button(self.result_frame, text="continue")
        self.result_button.pack()

        def edit_settings():
            game.settings = settings_gui(game.settings)

        # money frame
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)
        self.money_label = tk.Label(self.bottom_frame, text=f"Cash: ${game.player.get_money()}")
        self.profit_label = tk.Label(self.bottom_frame, text=f"Profit: ${game.player.get_profit()}")
        self.session_profit_label = tk.Label(self.bottom_frame, text=f"Session profit: ${game.player.get_profit(True)}")
        self.winstreak_label = tk.Label(self.bottom_frame, text=f"Winstreak: {game.player.stats.get_winstreak()}")
        self.winstreak_label.pack(side="bottom")
        self.session_profit_label.pack(side="bottom")
        self.profit_label.pack(side="bottom")
        self.money_label.pack(side="bottom")
        reset() # deleted duplicate code
        
        # preload all images
        for card, suit in deck_blueprint:
            image = get_image(card, suit)
        self.root.mainloop()