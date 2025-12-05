import json

def get_info():
    with open("save.json", "r") as file:
        return json.load(file)

def set_info(money, profit):
    data = {"money": money, "profit": profit}
    with open("save.json", "w") as file:
        json.dump(data, file, indent=4)
        return None