from modules.classes import Settings
from modules.file_adjuster import set_settings
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
            settings.cooldown = int(cooldown_entry.get())
            settings.deck_amount = int(deck_amount_entry.get())
        except Exception as err:
            error_label.config(text=f"{err}")
            return
        set_settings(settings)
        window.destroy()
    window = tk.Toplevel()
    window.geometry("500x200")

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

    error_label = tk.Label(window)

    save_button = tk.Button(window, text="save settings", command=on_save)
    save_button.pack(side="bottom")

    window.mainloop()
    return settings