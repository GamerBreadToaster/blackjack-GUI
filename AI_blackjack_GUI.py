import tkinter as tk
import random
import time
from modules.classes import Player, Dealer, Settings
from modules.image_adjuster import get_image
from modules.file_adjuster import get_info, set_info, get_settings
from modules.settings_GUI import settings_gui
from modules.score_calc import calculate_score, card_value

# Constants
CARD_CATEGORIES = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
CARDS_LIST = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
DECK_BLUEPRINT = [(card, category) for category in CARD_CATEGORIES for card in CARDS_LIST]


class Hand:
    """
    Represents a single hand of cards.
    Needed because a player might have multiple hands after splitting.
    """

    def __init__(self, bet):
        self.cards = []
        self.bet = bet
        self.is_finished = False  # If player stood or busted
        self.is_bust = False
        self.is_doubled = False

    def get_score(self):
        return calculate_score(self.cards)

    def add_card(self, card):
        self.cards.append(card)


class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Pro")

        # 1. Load Persistence Data
        self.data = get_info()
        self.data_settings = get_settings()

        # 2. Initialize Game Objects
        self.player = Player(self.data["money"], self.data["profit"])
        self.dealer = Dealer()
        self.settings = Settings(self.data_settings["cooldown"])

        # 3. Initialize Persistent Shoe (6 Decks)
        self.shoe = []
        self.reshuffle_shoe()

        # 4. Game State Variables
        self.player_hands = []  # List containing Hand objects
        self.current_hand_index = 0

        # 5. Build UI Layout
        self.screen_width = 600
        self.screen_height = 800
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.setup_ui()

        # 6. Start the Game Loop
        self.reset_game_state()

    def reshuffle_shoe(self):
        """Creates a new 6-deck shoe and shuffles it."""
        self.shoe = DECK_BLUEPRINT.copy() * 6
        random.shuffle(self.shoe)
        print("--- The shoe has been shuffled ---")

    def get_card_from_shoe(self):
        """Draws a card. Reshuffles if shoe is running low (< 20 cards)."""
        if len(self.shoe) < 20:
            self.reshuffle_shoe()
        return self.shoe.pop()

    def setup_ui(self):
        """Creates the main visual containers."""
        # -- Dealer Area --
        self.dealer_frame = tk.Frame(self.root, bg="green", pady=20)
        self.dealer_frame.pack(side="top", fill="x")
        self.dealer_score_label = tk.Label(self.root, text="Dealer Score:", bg="green", fg="white", font=("Arial", 12))
        self.dealer_score_label.pack()

        # -- Player Area (Container for multiple hands) --
        self.hands_container = tk.Frame(self.root, bg="#333", pady=20)
        self.hands_container.pack(side="top", fill="both", expand=True)

        # -- Controls Area --
        self.controls_frame = tk.Frame(self.root, pady=20)
        self.controls_frame.pack(fill="x")

        # -- Messages Area --
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), fg="red")
        self.result_label.pack(pady=5)

        # -- Stats/Money Area --
        self.bottom_frame = tk.Frame(self.root, pady=10)
        self.bottom_frame.pack(side="bottom", fill="x")

        self.money_label = tk.Label(self.bottom_frame, text=f"Cash: ${self.player.get_money()}", font=("Arial", 12))
        self.profit_label = tk.Label(self.bottom_frame, text=f"Profit: ${self.player.get_profit()}", font=("Arial", 12))
        self.money_label.pack(side="left", padx=20)
        self.profit_label.pack(side="right", padx=20)

        # Settings Button (Top Left)
        settings_btn = tk.Button(self.root, text="Settings", command=self.open_settings)
        settings_btn.place(x=10, y=10)

    def open_settings(self):
        # Using Toplevel for settings to avoid multiple root errors
        top = tk.Toplevel(self.root)
        top.title("Settings")
        settings_gui(
            self.settings)  # Note: You might need to adjust settings_gui to accept the 'top' window or handle destroy() differently
        top.destroy()

    def reset_game_state(self):
        """Resets the UI for the betting phase."""
        self.clear_table()
        self.player_hands = []
        self.dealer.cards = []
        self.current_hand_index = 0
        self.result_label.config(text="Place your bet!")

        # Create Betting Controls
        self.bet_entry = tk.Entry(self.controls_frame, width=10, font=("Arial", 12))
        self.bet_entry.insert(0, str(self.player.original_bet if self.player.original_bet > 0 else 10))
        self.bet_entry.pack(side="left", padx=5)

        self.deal_button = tk.Button(self.controls_frame, text="DEAL", bg="gold", command=self.deal_initial_cards)
        self.deal_button.pack(side="left", padx=5)

        self.bet_entry.bind("<Return>", lambda e: self.deal_initial_cards())
        self.bet_entry.focus_set()

    def clear_table(self):
        """Removes card images and buttons."""
        for widget in self.dealer_frame.winfo_children(): widget.destroy()
        for widget in self.hands_container.winfo_children(): widget.destroy()
        for widget in self.controls_frame.winfo_children(): widget.destroy()

    def deal_initial_cards(self):
        """Starts the round."""
        # 1. Validate Bet
        try:
            bet_amount = int(self.bet_entry.get())
            if bet_amount > self.player.get_money():
                self.result_label.config(text="Insufficient Funds!")
                return
            if bet_amount <= 0:
                self.result_label.config(text="Bet must be > 0")
                return
        except ValueError:
            self.result_label.config(text="Invalid Bet")
            return

        # 2. Deduct Money
        self.player.original_bet = bet_amount
        self.player.adjust_money(-bet_amount)
        set_info(self.player)
        self.update_stats()

        # 3. Create Main Hand and Deal
        main_hand = Hand(bet_amount)
        main_hand.add_card(self.get_card_from_shoe())  # Player card 1
        self.dealer.cards.append(self.get_card_from_shoe())  # Dealer card 1
        main_hand.add_card(self.get_card_from_shoe())  # Player card 2
        self.dealer.cards.append(self.get_card_from_shoe())  # Dealer card 2

        self.player_hands.append(main_hand)

        # 4. Render
        self.clear_table()
        self.render_hands()

        # 5. Check Initial Blackjack (Dealer or Player)
        player_score = main_hand.get_score()
        dealer_up_card_val = card_value(self.dealer.cards[0])

        # Simple check: if player has 21, round ends immediately (unless dealer also has 21, handled in results)
        if player_score == 21:
            self.handle_dealer_turn()
            return

        # 6. Show Buttons
        self.show_game_controls()

    def render_hands(self):
        """
        Draws all cards.
        Crucial: It highlights the 'active' hand so the player knows which one they are playing.
        """
        # Clear Display
        for widget in self.hands_container.winfo_children(): widget.destroy()
        for widget in self.dealer_frame.winfo_children(): widget.destroy()

        # --- Draw Dealer ---
        # If player is done with ALL hands, reveal dealer's hole card
        is_dealer_turn = (self.current_hand_index >= len(self.player_hands))

        if is_dealer_turn:
            for card in self.dealer.cards:
                self.add_card_image(card, self.dealer_frame)
            self.dealer_score_label.config(text=f"Dealer Score: {self.dealer.get_score()}")
        else:
            # Hide second card
            self.add_card_image(self.dealer.cards[0], self.dealer_frame)
            self.add_card_image("joker", self.dealer_frame)
            self.dealer_score_label.config(text=f"Dealer Score: {card_value(self.dealer.cards[0])}")

        # --- Draw Player Hands ---
        for i, hand in enumerate(self.player_hands):
            # Each hand gets its own Frame
            hand_frame = tk.Frame(self.hands_container, bd=3, relief="raised", padx=10, pady=10)
            hand_frame.pack(side="left", padx=10, pady=10)

            # VISUAL CUE: Highlight the active hand in Yellow
            if i == self.current_hand_index and not is_dealer_turn:
                hand_frame.config(bg="#ffffcc")
                tk.Label(hand_frame, text="CURRENT HAND", bg="#ffffcc", fg="red", font=("Arial", 8, "bold")).pack(
                    side="top")

            # Draw cards
            card_row = tk.Frame(hand_frame, bg=hand_frame.cget('bg'))
            card_row.pack()
            for card in hand.cards:
                self.add_card_image(card, card_row)

            # Info labels
            status = f"Score: {hand.get_score()}"
            if hand.is_bust: status += " (BUST)"
            tk.Label(hand_frame, text=status, bg=hand_frame.cget('bg')).pack(side="bottom")
            tk.Label(hand_frame, text=f"Bet: ${hand.bet}", bg=hand_frame.cget('bg')).pack(side="bottom")

    def add_card_image(self, card, frame):
        if card == "joker":
            img = get_image("joker", "joker")
        else:
            img = get_image(card[0], card[1])
        lbl = tk.Label(frame, image=img, bg=frame.cget('bg'))
        lbl.image = img  # Reference needed!
        lbl.pack(side="left", padx=2)

    def show_game_controls(self):
        """Shows Hit, Stand, Double, Split buttons based on rules."""
        for widget in self.controls_frame.winfo_children(): widget.destroy()

        if self.current_hand_index >= len(self.player_hands):
            return  # Should be dealer's turn

        current_hand = self.player_hands[self.current_hand_index]

        # Standard Buttons
        tk.Button(self.controls_frame, text="HIT", width=10, command=self.hit).pack(side="left", padx=5)
        tk.Button(self.controls_frame, text="STAND", width=10, command=self.stand).pack(side="left", padx=5)

        # DOUBLE Logic
        if len(current_hand.cards) == 2 and self.player.get_money() >= current_hand.bet:
            tk.Button(self.controls_frame, text="DOUBLE", width=10, command=self.double).pack(side="left", padx=5)

        # SPLIT Logic
        if len(current_hand.cards) == 2 and self.player.get_money() >= current_hand.bet:
            val1 = card_value(current_hand.cards[0])
            val2 = card_value(current_hand.cards[1])
            # Check for pair (same value, e.g. 10 and King, or 8 and 8)
            if val1 == val2:
                tk.Button(self.controls_frame, text="SPLIT", width=10, bg="lightblue", command=self.split).pack(
                    side="left", padx=5)

    def hit(self):
        hand = self.player_hands[self.current_hand_index]
        hand.add_card(self.get_card_from_shoe())
        self.render_hands()

        if hand.get_score() > 21:
            hand.is_bust = True
            hand.is_finished = True
            # Delay slightly so user sees the bust card before switching hands
            self.root.after(500, self.next_hand)
        elif hand.get_score() == 21:
            hand.is_finished = True
            self.root.after(500, self.next_hand)

    def stand(self):
        self.player_hands[self.current_hand_index].is_finished = True
        self.next_hand()

    def double(self):
        hand = self.player_hands[self.current_hand_index]
        self.player.adjust_money(-hand.bet)  # Pay extra bet
        hand.bet *= 2
        hand.is_doubled = True

        # One card only
        hand.add_card(self.get_card_from_shoe())
        hand.is_finished = True

        if hand.get_score() > 21:
            hand.is_bust = True

        self.render_hands()
        self.update_stats()
        self.root.after(self.settings.cooldown, self.next_hand)

    def split(self):
        current_hand = self.player_hands[self.current_hand_index]

        # 1. Deduct money for the new split bet
        self.player.adjust_money(-current_hand.bet)

        # 2. Separate the cards
        split_card = current_hand.cards.pop()  # Remove 2nd card

        # 3. Create the new Hand object
        new_hand = Hand(current_hand.bet)
        new_hand.add_card(split_card)

        # 4. Hit both hands once automatically (standard blackjack rule)
        current_hand.add_card(self.get_card_from_shoe())
        new_hand.add_card(self.get_card_from_shoe())

        # 5. Add the new hand to the list immediately after the current one
        self.player_hands.insert(self.current_hand_index + 1, new_hand)

        self.update_stats()
        self.render_hands()
        self.show_game_controls()  # Refresh buttons (allows re-splitting if implemented)

    def next_hand(self):
        """Iterates to the next player hand. If done, triggers Dealer."""
        self.current_hand_index += 1

        if self.current_hand_index < len(self.player_hands):
            # Play the next hand in the list
            self.render_hands()
            self.show_game_controls()
        else:
            # Finished all hands -> Dealer Turn
            self.handle_dealer_turn()

    def handle_dealer_turn(self):
        self.render_hands()  # This will now reveal the hole card

        # Optimization: If all player hands busted, Dealer doesn't need to hit.
        all_busted = all(h.is_bust for h in self.player_hands)

        if not all_busted:
            # Dealer hits on anything below 17
            self.dealer_hit_loop()
        else:
            self.calculate_results()

    def dealer_hit_loop(self):
        """Recursive loop with delay for animation effect."""
        if self.dealer.get_score() < 17:
            self.dealer.cards.append(self.get_card_from_shoe())
            self.render_hands()
            # Call this function again after delay
            self.root.after(self.settings.cooldown, self.dealer_hit_loop)
        else:
            self.calculate_results()

    def calculate_results(self):
        dealer_score = self.dealer.get_score()
        total_payout = 0
        results_summary = ""

        for i, hand in enumerate(self.player_hands):
            # Blackjack Payout (3:2) - only if 2 cards and 21 (and not split usually, but let's keep it simple)
            is_blackjack = (hand.get_score() == 21 and len(hand.cards) == 2)

            outcome = ""

            if hand.is_bust:
                outcome = "Bust"
            elif is_blackjack and dealer_score != 21:
                outcome = "Blackjack!"
                total_payout += hand.bet + (hand.bet * 1.5)
            elif dealer_score > 21:
                outcome = "Win (Dealer Bust)"
                total_payout += hand.bet * 2
            elif hand.get_score() > dealer_score:
                outcome = "Win"
                total_payout += hand.bet * 2
            elif hand.get_score() == dealer_score:
                outcome = "Push"
                total_payout += hand.bet  # Return original bet
            else:
                outcome = "Lose"

            results_summary += f"Hand {i + 1}: {outcome}\n"

        self.player.adjust_money(total_payout)
        self.update_stats()
        self.result_label.config(text=results_summary)

        # Show "New Round" button
        for widget in self.controls_frame.winfo_children(): widget.destroy()
        tk.Button(self.controls_frame, text="NEW ROUND", bg="lightgreen", height=2, width=20,
                  command=self.reset_game_state).pack()

    def update_stats(self):
        self.money_label.config(text=f"Cash: ${self.player.get_money()}")
        self.profit_label.config(text=f"Profit: ${self.player.get_profit()}")
        set_info(self.player)


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()