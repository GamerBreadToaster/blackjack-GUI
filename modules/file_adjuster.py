import os.path

from modules.classes import Player, Settings, Dealer, Result
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

def add_history(result: Result):
    # this saves a list of all played games
    file_path = "history.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {"games": []}
    else:
        data = {"games": []}

    data["games"].append(result.to_dict())
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)