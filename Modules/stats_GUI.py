import tkinter as tk
from Modules.debug import log, DEBUG_MODE
from Modules.image_adjuster import add_card
from Modules.file_adjuster import get_history
from datetime import datetime
import math

# almost Fully AI generated because I didn't know what the fuck I was doing

def stats_gui():
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def __add_frame(parent: tk.Misc, game_data):
        # Container for a single game history entry
        # Adding a ridge border to clearly separate each game
        game_container = tk.Frame(parent, bd=4, relief="ridge", pady=10)
        game_container.pack(fill="x", pady=10, padx=10)

        # time played for each game
        dt_object = datetime.fromtimestamp(game_data["time"])
        formatted_time = dt_object.strftime("%H:%M:%S | %d/%m/%Y")
        time_played_label = tk.Label(game_container, text=f"played at: {formatted_time}")
        time_played_label.pack()

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
        window.geometry("525x200")
        tk.Label(window, text="No games played yet!", font=("Arial", 14)).pack(expand=True)
        return

    # --- Pre-calculate Window Size ---
    max_cards_ever = 0
    for game in history["games"]:
        highest_in_game = max(len(game["player_cards"]), len(game["dealer_cards"]))
        if highest_in_game > max_cards_ever:
            max_cards_ever = highest_in_game

    req_length = int(len(history["games"]) / 25)

    req_width = max(525, max_cards_ever * 125 + 25)
    screen_size = {"width": req_width, "height": 800 + req_length}

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
    # I have no idea what I'm doing here, which is obvious
    # global counter, max_counter
    # max_counter = len(history["games"])
    # counter = max_counter - 10
    # def add_games():
    #     global counter, max_counter
    #     if counter < 1:
    #         # more_button.config(state="disabled")
    #         counter = 0
    #     for i in reversed(range(counter, max_counter)):
    #         game = history["games"][i]
    #         log(f"Making game: {i + 1}, max amount of games: {max_counter}")
    #         __add_frame(scrollable_frame, game)
    #     counter -= 10
    #     max_counter -= 10

    def __add_buttons(frame_number):
        def __add_button(frame, page):
            button = tk.Button(frame, text=str(page), command=lambda: __add_games(page))
            button.pack(side="left", padx=5, pady=5)

        frame = tk.Frame(window)
        frame.pack(fill="x")

        amount_pages = len(history["games"]) / 10 + 1
        if amount_pages < 1:
            amount_pages = 1

        amount_pages = min(math.ceil(amount_pages), frame_number * 10)
        min_pages = (frame_number - 1) * 10 + 1

        for i in range(min_pages, amount_pages):
            __add_button(frame, i)


    def __add_games(page: int):
        for child in scrollable_frame.winfo_children():
            child.destroy()

        amount_games = len(history["games"])
        max_counter = amount_games - (page * 10 - 10)
        min_counter = amount_games - page * 10
        if max_counter < 0:
            max_counter = 0

        for index_game in reversed(range(min_counter, max_counter)):
            game = history["games"][index_game]
            log(f"Making game: {index_game + 1}, max amount of games: {max_counter}")
            __add_frame(scrollable_frame, game)

    __add_games(1)

    max_frames = math.ceil(len(history["games"]) / 100)

    for i in range(1, max_frames + 1):
        __add_buttons(i)

    canvas.bind_all("<MouseWheel>", _on_mousewheel)