import tkinter as tk
from Modules.image_adjuster import add_card
from Modules.file_adjuster import get_history

# thanks, AI, for doing this for me sigh.

def stats_gui():
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def __add_frame(parent: tk.Misc, game_data):
        # Container for a single game history entry
        # Adding a ridge border to clearly separate each game
        game_container = tk.Frame(parent, bd=4, relief="ridge", pady=10)
        game_container.pack(fill="x", pady=10, padx=10)

        # --- Dealer Frame (Green) ---
        dealer_frame = tk.Frame(game_container, bg="green", pady=10)
        dealer_frame.pack(side="top", fill="x")

        dealer_score_label = tk.Label(dealer_frame, text=f"Dealer Score: {game_data['dealer_score']}", bg="green",
                                      fg="white", font=("Arial", 12, "bold"))
        dealer_score_label.pack(side="top")

        # A sub-frame just for holding the cards horizontally
        dealer_cards_frame = tk.Frame(dealer_frame, bg="green")
        dealer_cards_frame.pack(side="top")
        for card in game_data["dealer_cards"]:
            # Note: Passing window and screen_size to match your current image_adjuster.py
            add_card(card, dealer_cards_frame)

        # --- Player Frame (Red) ---
        player_frame = tk.Frame(game_container, bg="red", pady=10)
        player_frame.pack(side="top", fill="x")

        player_score_label = tk.Label(player_frame, text=f"Player Score: {game_data['player_score']}", bg="red",
                                      fg="white", font=("Arial", 12, "bold"))
        player_score_label.pack(side="top")

        player_cards_frame = tk.Frame(player_frame, bg="red")
        player_cards_frame.pack(side="top")
        for card in game_data["player_cards"]:
            add_card(card, player_cards_frame)

        # --- Result Frame (Bottom) ---
        result_frame = tk.Frame(game_container, pady=10)
        result_frame.pack(side="top", fill="x")

        # Recreating the exact result label from the main game
        result_label = tk.Label(result_frame, text=game_data["message"], font=("Arial", 14, "bold"), fg="red")
        result_label.pack(side="top")

        # Extra context: showing the bet amount and if they doubled down
        double_str = " (Doubled Down)" if game_data.get("double_down") else ""
        bet_label = tk.Label(result_frame, text=f"Bet: ${game_data['bet']}{double_str}", font=("Arial", 10, "italic"))
        bet_label.pack(side="top")

    history = get_history()

    # Quick safeguard in case the user opens stats before playing any games
    if not history or "games" not in history or not history["games"]:
        window = tk.Toplevel()
        window.title("Game History")
        window.geometry("400x200")
        tk.Label(window, text="No games played yet!", font=("Arial", 14)).pack(expand=True)
        return

    # --- Pre-calculate Window Size ---
    max_cards_ever = 0
    for game in history["games"]:
        highest_in_game = max(len(game["player_cards"]), len(game["dealer_cards"]))
        if highest_in_game > max_cards_ever:
            max_cards_ever = highest_in_game

    req_width = max(500, max_cards_ever * 125)
    screen_size = {"width": req_width, "height": 800}

    # --- Main Stats Window Setup ---
    window = tk.Toplevel()
    window.geometry(f"{screen_size['width']}x{screen_size['height']}")
    window.title("Game History")

    # Set up scrolling canvas
    container = tk.Frame(window)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Draw the games in reverse order so the newest games are at the top!
    for game in reversed(history["games"]):
        __add_frame(scrollable_frame, game)

    canvas.bind_all("<MouseWheel>", _on_mousewheel)