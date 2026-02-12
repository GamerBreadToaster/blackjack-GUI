from Modules.file_adjuster import get_history
from Modules.classes import ResultType

data = get_history()
for game in data["games"]:
    game["win_type"] = ResultType(game["win_type"] )
    print(game)