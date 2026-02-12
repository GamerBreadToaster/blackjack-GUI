from modules.classes import Player, Settings, Dealer
import json

def get_info():
    try:
        with open("save.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open("save.json", "w") as file:
            data = {
                "money": 2500,
                "profit": 0
            }
            json.dump(data, file, indent=2)
            return data

def set_info(player: Player):
    data = {
        "money": player.get_money(),
        "profit": player.get_profit(),
        "stats": player.stats.to_dict()
    }
    with open("save.json", "w") as file:
        json.dump(data, file, indent=2)
        return None

def set_settings(settings: Settings):
    data = settings.to_dict()
    with open("settings.json", "w") as file:
        json.dump(data, file, indent=2)
        return None

def get_settings():
    try:
        with open("settings.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open("settings.json", "w") as file:
            data = {
                "cooldown": 750,
                "deck_amount": 6
            }
            json.dump(data, file, indent=2)
            return data

# def add_history(player: Player, dealer: Dealer, settings: Settings):
#     try:
#         with open("history.json", "rw") as file:
#             pass
#