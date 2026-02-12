from modules.classes import Player, Dealer, Result, ResultType

def check_scores(player: Player, dealer: Dealer):
    if player.get_score() > 21:
        result_type = ResultType.PLAYER_BUST
    elif dealer.get_score() > 21:
        result_type = ResultType.DEALER_BUST
    elif player.get_score() == dealer.get_score():
        result_type = ResultType.PUSH
    elif player.get_score() > dealer.get_score():
        result_type = ResultType.PLAYER_HIGHER
    elif player.get_score() < dealer.get_score():
        result_type = ResultType.DEALER_HIGHER
    else:
        raise Exception("Something with checking scores went wrong")
    result = Result(player, dealer, result_type)

    return result