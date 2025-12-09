from modules.players import Player, Settings
import json

def get_info():
    try:
        with open("save.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open("save.json", "w") as file:
            data = {
                "money": 2500,
                "profit": 0,
                "cooldown": 750
            }
            json.dump(data, file, indent=2)
            return data

def set_info(player: Player, settings: Settings):
    data = {
        "money": player.get_money(),
        "profit": player.get_profit(),
        "cooldown": settings.cooldown
    }
    with open("save.json", "w") as file:
        json.dump(data, file, indent=2)
        return None