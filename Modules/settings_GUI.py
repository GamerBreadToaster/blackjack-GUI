from Modules.classes import Settings
from Modules.file_adjuster import set_settings
import tkinter as tk
def settings_gui(settings: Settings) -> Settings:
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
            settings.cooldown = int(cooldown_entry.get())
            settings.deck_amount = int(deck_amount_entry.get())
            if settings.deck_amount < 1:
                raise Exception("Deck amount should be at least one (1)!")
            settings.dealer_stop = int(dealer_stop_entry.get())
            if settings.dealer_stop < 1:
                raise Exception("dealer stop should be at least one (1)!")
            settings.credit_card_debt = float(credit_card_entry.get())
            if settings.credit_card_debt < 1:
                raise Exception("Credit card usage should at least be one (1)")
            settings.max_score = int(max_score_entry.get())
            if settings.max_score < 1:
                raise Exception("Max score should be at least one (1)")
        except Exception as err:
            error_label.config(text=f"{err}")
            return
        set_settings(settings)
        window.destroy()
    window = tk.Toplevel()

    cooldown_entry = __add_labeled_field(
        window,
        "General cooldown in ms: ",
        settings.cooldown
    )
    deck_amount_entry = __add_labeled_field(
        window,
        "Total amount of decks used: \n(Gets shuffled after every round)",
        settings.deck_amount
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
    enable_blackjack_var = tk.BooleanVar(value=settings.enable_blackjack)
    enable_blackjack_button = tk.Checkbutton(window, text="Enable blackjack", variable=enable_blackjack_var)
    enable_blackjack_button.pack()

    error_label = tk.Label(window)
    error_label.pack()

    save_button = tk.Button(window, text="save settings", command=on_save)
    save_button.pack(side="bottom")

    return settings