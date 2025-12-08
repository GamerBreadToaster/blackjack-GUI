import os
from PIL import Image, ImageTk

image_cache = {} # Global dictionary to store loaded images
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)

def get_image(card, suite) -> ImageTk.PhotoImage | None:
    card = card.lower()
    suite = suite.lower()
    key = f"{card}_{suite}"

    if key in image_cache:
        return image_cache[key] # idea by Gemini

    path = os.path.join(project_root, "cards", f"{card}_of_{suite}")
    if card in ['jack', 'king', 'queen']:
        path += "2.png" # uses the better looking cards
    elif card == "joker": # Joker is the unknown card
        path = os.path.join(os.getcwd(), "cards", "red_joker.png")
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