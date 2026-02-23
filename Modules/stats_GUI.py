from Modules.classes import Stats
import tkinter as tk
from Modules.image_adjuster import add_card
from Modules.file_adjuster import get_history

# def stats_gui(stats: Stats):
#     window = tk.Toplevel()
#     window.title("Stats")
#     win_frame = tk.Frame(window, bg="green")
#     lose_frame = tk.Frame(window, bg="red")
#     win_frame.pack(side="left", fill="x")
#     lose_frame.pack(side="right", fill="x")
#
#     # win frame
#     total_won_label = tk.Label(win_frame, text=f"Total money won: ${stats.total_won}", bg="green", fg="white")
#     blackjack_won_label = tk.Label(win_frame, text=f"Total blackjacks won: {stats.won_by_blackjack}", bg="green", fg="white")
#     higher_score_label = tk.Label(win_frame, text=f"Total times you won by having a higher score: {stats.higher_score}", bg="green", fg="white")
#     dealer_bust_label = tk.Label(win_frame, text=f"Total times the dealer busted: {stats.dealer_bust}", bg="green", fg="white")
#     total_games_won_label = tk.Label(win_frame, text=f"Total games won: {stats.total_games_won()}", bg="green", fg="white")
#     total_won_label.pack()
#     blackjack_won_label.pack()
#     higher_score_label.pack()
#     dealer_bust_label.pack()
#     total_games_won_label.pack()
#
#     # lose frame
#     total_lost_label = tk.Label(lose_frame, text=f"Total money lost: ${stats.total_lost}", bg="red", fg="white")
#     blackjack_lost_label = tk.Label(lose_frame, text=f"Total blackjacks lost: {stats.lost_by_blackjack}", bg="red", fg="white")
#     lower_score_label = tk.Label(lose_frame, text=f"Total times you lost by having a lower score: {stats.lower_score}", bg="red", fg="white")
#     player_bust_label = tk.Label(lose_frame, text=f"Total times you busted: {stats.player_bust}", bg="red", fg="white")
#     total_games_lost_label = tk.Label(lose_frame, text=f"Total games lost: {stats.total_games_lost()}", bg="red", fg="white")
#     total_lost_label.pack()
#     blackjack_lost_label.pack()
#     lower_score_label.pack()
#     player_bust_label.pack()
#     total_games_lost_label.pack()
#
#     # under the frames
#     double_down_label = tk.Label(window, text=f"Total times you doubled down: {stats.double_downs}")
#     double_down_label.pack()
#     ties_label = tk.Label(window, text=f"Total times you got pushed: {stats.ties}")
#     ties_label.pack()
#     total_credit_card_use_label = tk.Label(window, text=f"Total creditcard uses: {stats.used_credit_card}")
#     total_credit_card_use_label.pack()
#     blackjack_ties_label = tk.Label(window, text=f"Total times you got blackjack pushed: {stats.blackjack_push}")
#     blackjack_ties_label.pack()
#     total_games_label = tk.Label(window, text=f"Total games played: {stats.total_games()}")
#     total_games_label.pack()
#     winstreak_label = tk.Label(window, text=f"Current winstreak: {stats.winstreak} wins")
#     winstreak_label.pack()
#     hit_21_label = tk.Label(window, text=f"Total times you hit exactly 21: {stats.hit_21}")
#     hit_21_label.pack()
#
#     window.mainloop()

games = {
      "player_cards": [
        [
          "2",
          "Clubs"
        ],
        [
          "King",
          "Hearts"
        ],
        [
          "3",
          "Diamonds"
        ],
        [
          "4",
          "Diamonds"
        ]
      ],
      "dealer_cards": [
        [
          "10",
          "Clubs"
        ],
        [
          "Queen",
          "Diamonds"
        ]
      ],
      "player_score": 19,
      "dealer_score": 20,
      "bet": 100.0,
      "double_down": False,
      "win_type": "DEALER_HIGHER",
      "message": "Your score is lower! You lose $100.0!"
    }

def stats_gui():
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def __add_frame(parent: tk.Misc, game_data):
        game_container = tk.Frame(parent, bd=2, relief="groove", pady=10)
        game_container.pack(fill="x", pady=5, padx=5)
        dealer_frame = tk.Frame(game_container, bg="green", pady=20)
        dealer_frame.pack(side="top", fill="x")
        dealer_score_label = tk.Label(game_container, name="dealer_score", text=f"Dealer Score: {game_data["dealer_score"]}", bg="green")
        dealer_score_label.pack()
        for card in game_data["dealer_cards"]:
            add_card(card, dealer_frame, game_container, screen_size)

        player_frame = tk.Frame(game_container, bg="red", pady=20)
        player_frame.pack(side="top", fill="x")
        player_score_label = tk.Label(game_container, name="player_score", text=f"Player Score: {game_data["player_score"]}", bg="red")
        player_score_label.pack()
        for card in game_data["player_cards"]:
            add_card(card, player_frame, game_container, screen_size)

    history = get_history()
    screen_size = {"width": 500, "height": 800}
    window = tk.Toplevel()
    window.geometry(f"{screen_size["width"]}x{screen_size["height"]}")
    window.title("Stats")

    container = tk.Frame(window)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    # thanks AI
    # This magic line updates the scroll region whenever the frame grows
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="bottom", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for games in history["games"]:
        __add_frame(container, games)

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    window.mainloop()