from modules.classes import Stats
import tkinter as tk

def stats_gui(stats: Stats):
    window = tk.Toplevel()
    window.title("Stats")
    win_frame = tk.Frame(window, bg="green")
    lose_frame = tk.Frame(window, bg="red")
    win_frame.pack(side="left", fill="x")
    lose_frame.pack(side="right", fill="x")

    # win frame
    total_won_label = tk.Label(win_frame, text=f"Total money won: ${stats.total_won}", bg="green")
    blackjack_won_label = tk.Label(win_frame, text=f"Total blackjacks won: {stats.won_by_blackjack}", bg="green")
    higher_score_label = tk.Label(win_frame, text=f"Total times you won by having a higher score: {stats.higher_score}", bg="green")
    dealer_bust_label = tk.Label(win_frame, text=f"Total times the dealer busted: {stats.dealer_bust}", bg="green")
    total_games_won_label = tk.Label(win_frame, text=f"Total games won: {stats.total_games_won()}", bg="green")
    total_won_label.pack()
    blackjack_won_label.pack()
    higher_score_label.pack()
    dealer_bust_label.pack()
    total_games_won_label.pack()

    # lose frame
    total_lost_label = tk.Label(lose_frame, text=f"Total money lost: ${stats.total_lost}", bg="red")
    blackjack_lost_label = tk.Label(lose_frame, text=f"Total blackjacks lost: {stats.lost_by_blackjack}", bg="red")
    lower_score_label = tk.Label(lose_frame, text=f"Total times you lost by having a lower score: {stats.lower_score}", bg="red")
    player_bust_label = tk.Label(lose_frame, text=f"Total times you busted: {stats.player_bust}", bg="red")
    total_games_lost_label = tk.Label(lose_frame, text=f"Total games lost: {stats.total_games_lost()}", bg="red")
    total_lost_label.pack()
    blackjack_lost_label.pack()
    lower_score_label.pack()
    player_bust_label.pack()
    total_games_lost_label.pack()

    # under the frames
    double_down_label = tk.Label(window, text=f"Total times you doubled down: {stats.double_downs}")
    double_down_label.pack()
    ties_label = tk.Label(window, text=f"Total times you got pushed: {stats.ties}")
    ties_label.pack()
    total_games_label = tk.Label(window, text=f"Total games played: {stats.total_games()}")
    total_games_label.pack()

    window.mainloop()