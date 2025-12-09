from modules.players import Player, Settings
import json

def get_info():
    with open("save.json", "r") as file:
        return json.load(file)

def set_info(player: Player, settings: Settings):
    data = {
        "money": player.get_money(),
        "profit": player.get_profit(),
        "cooldown": settings.cooldown
    }
    with open("save.json", "w") as file:
        json.dump(data, file, indent=4)
        return None