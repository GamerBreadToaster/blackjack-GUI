from modules.players import Settings
from modules.file_adjuster import set_settings
import tkinter as tk
def settings_gui(settings: Settings) -> Settings:
    def save():
        try:
            settings.cooldown = int(cooldown_entry.get())
        except Exception as err:
            error_label.config(text=f"{err}")
            return
        set_settings(settings)
        root.destroy()
    root = tk.Tk()
    root.geometry("500x200")

    cooldown_frame = tk.Frame(root)
    cooldown_label = tk.Label(cooldown_frame, text="General cooldown in ms: ")
    cooldown_entry = tk.Entry(cooldown_frame)
    cooldown_entry.insert(0, settings.cooldown)
    cooldown_label.pack(side="left")
    cooldown_entry.pack(side="left")
    cooldown_frame.pack()

    error_label = tk.Label(root)

    save_button = tk.Button(root, text="save settings", command=save)
    save_button.pack(side="bottom")

    root.mainloop()
    return settings