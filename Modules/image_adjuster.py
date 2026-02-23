import os
from PIL import Image, ImageTk
import tkinter as tk

image_cache = {} # Global dictionary to store loaded images
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)

def get_image(card, suite) -> ImageTk.PhotoImage | None:
    card = card.lower()
    suite = suite.lower()
    key = f"{card}_{suite}"

    if key in image_cache:
        return image_cache[key] # idea by Gemini

    path = os.path.join(project_root, "Cards", f"{card}_of_{suite}")
    if card in ['jack', 'king', 'queen']:
        path += "2.png" # uses the better looking Cards
    elif card == "joker": # Joker is the unknown card
        path = os.path.join(os.getcwd(), "Cards", "red_joker.png")
    else:
        path += ".png"
    try:
        image = Image.open(path).resize((100, 145))
        photo = ImageTk.PhotoImage(image)
        image_cache[key] = photo
        return photo
    except FileNotFoundError as err:
        print("error:",err)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")

def add_card(card, frame, root, screen_size):
    if not card == "joker":
        image = get_image(card[0], card[1])
    else:
        # joker is a placeholder name for an empty card
        image = get_image("joker", "joker")
    card_label = tk.Label(frame, image=image)
    card_label.image = image
    card_amount = len(frame.winfo_children())
    if card_amount > 4:
        if not screen_size['width'] > card_amount * 125:
            screen_size['width'] = card_amount * 125
        root.geometry(f"{screen_size['width']}x{screen_size['height']}")
        root.update()
    card_label.pack(side="left", padx=10)