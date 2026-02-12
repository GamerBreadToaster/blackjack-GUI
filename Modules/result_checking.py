from Modules.classes import Player, Dealer, Result, ResultType

def check_scores(player: Player, dealer: Dealer) -> Result:
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
    return Result(player, dealer, result_type)

def check_blackjack(player: Player, dealer: Dealer) -> Result:
    if player.get_score() == dealer.get_score():
        result_type = ResultType.PUSH_BLACKJACK
    elif player.get_score() == 21:
        result_type = ResultType.PLAYER_BLACKJACK
    elif dealer.get_score() == 21:
        result_type = ResultType.DEALER_BLACKJACK
    else:
        result_type = ResultType.NONE

    return Result(player, dealer, result_type)
