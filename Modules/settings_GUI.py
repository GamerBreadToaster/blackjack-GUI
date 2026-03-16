from Modules.classes import Settings
from Modules.file_adjuster import set_settings
import tkinter as tk
def settings_gui(settings: Settings) -> Settings:
    def reset_settings():
        settings.cooldown = 750
        settings.deck_amount = 6
        settings.shuffle_after = 5
        settings.dealer_stop = 17
        settings.credit_card_debt = 1000
        settings.max_score = 21
        settings.enable_blackjack = True
        settings.stand_at_max = True
        set_settings(settings)
        window.destroy()
    def __add_labeled_field(parent: tk.Misc, label_text: str, initial_value) -> tk.Entry:
        frame = tk.Frame(parent)
        label = tk.Label(frame, text=label_text)
        entry = tk.Entry(frame)
        entry.insert(0, str(initial_value))

        label.pack(side="left")
        entry.pack(side="left")
        frame.pack(anchor="w", padx=10, pady=6)

        return entry

    def on_save():
        try:
            settings.enable_blackjack = enable_blackjack_var.get()
            settings.stand_at_max = stand_at_max_var.get()
            settings.cooldown = int(cooldown_entry.get())
            settings.deck_amount = int(deck_amount_entry.get())
            if settings.deck_amount < 1:
                raise Exception("Deck amount should be at least one (1)!")
            settings.shuffle_after = int(shuffle_at_entry.get())
            if settings.shuffle_after < 1:
                raise Exception("Shuffle after should be at least one (1)!")
            settings.dealer_stop = int(dealer_stop_entry.get())
            if settings.dealer_stop < 1:
                raise Exception("dealer stop should be at least one (1)!")
            settings.credit_card_debt = float(credit_card_entry.get())
            if settings.credit_card_debt < 1:
                raise Exception("Credit card usage should at least be one (1)!")
            settings.max_score = int(max_score_entry.get())
            if settings.max_score < 1:
                raise Exception("Max score should be at least one (1)!")
        except Exception as err:
            error_label.config(text=f"{err}")
            return
        set_settings(settings)
        window.destroy()
    window = tk.Toplevel()
    window.grab_set()

    cooldown_entry = __add_labeled_field(
        window,
        "General cooldown in ms: ",
        settings.cooldown
    )
    deck_amount_entry = __add_labeled_field(
        window,
        f"Total number of decks used: \n(Gets shuffled after every {settings.shuffle_after} round(s))",
        settings.deck_amount
    )
    shuffle_at_entry = __add_labeled_field(
        window,
        "Shuffle after this many rounds: ",
        settings.shuffle_after
    )
    dealer_stop_entry = __add_labeled_field(
        window,
        "Dealer stops at this score: \n(will break balance unless 17)",
        settings.dealer_stop
    )
    credit_card_entry = __add_labeled_field(
        window,
        "How much money you'll take from your credit card:",
        settings.credit_card_debt
    )
    max_score_entry = __add_labeled_field(
        window,
        "Maximum score you can win: \n(At what score anyone will bust)",
        settings.max_score
    )
    stand_at_max_var = tk.BooleanVar(value=settings.stand_at_max)
    stand_at_max_button = tk.Checkbutton(window, text="automatically stand at max score", variable=stand_at_max_var)
    stand_at_max_button.pack()
    enable_blackjack_var = tk.BooleanVar(value=settings.enable_blackjack)
    enable_blackjack_button = tk.Checkbutton(window, text="Enable blackjack", variable=enable_blackjack_var)
    enable_blackjack_button.pack()

    error_label = tk.Label(window)
    error_label.pack()

    reset_settings = tk.Button(window, text="reset settings to default", command=reset_settings)
    reset_settings.pack(side="bottom")
    save_button = tk.Button(window, text="save settings", command=on_save)
    save_button.pack(side="bottom")

    window.wait_window()

    return settings