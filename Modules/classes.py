from Modules.score_calc import calculate_score, card_value
from enum import Enum, auto
# stats
class Stats:
    def __init__(self, total_won: float = 0.0, total_lost: float = 0.0, ties: int = 0, won_by_blackjack: int = 0, lost_by_blackjack: int = 0,
                 higher_score: int = 0, lower_score: int = 0, used_credit_card: int = 0, double_downs: int = 0, player_bust: int = 0,
                 dealer_bust: int = 0, blackjack_push: int = 0, winstreak = 0, hit_21 = 0, **kwargs):
        self.total_won = total_won
        self.total_lost = total_lost
        self.won_by_blackjack = won_by_blackjack
        self.lost_by_blackjack = lost_by_blackjack
        self.higher_score = higher_score
        self.lower_score = lower_score
        self.player_bust = player_bust
        self.dealer_bust = dealer_bust
        self.used_credit_card = used_credit_card
        self.ties = ties
        self.double_downs = double_downs
        self.blackjack_push = blackjack_push
        self.winstreak = winstreak
        self.hit_21 = hit_21

    def total_games(self) -> int:
        return self.total_games_won() + self.total_games_lost() + self.ties

    def total_games_won(self):
        return self.won_by_blackjack + self.higher_score + self.dealer_bust

    def total_games_lost(self):
        return self.lost_by_blackjack + self.lower_score + self.player_bust

    def to_dict(self):
        """Helper to turn this object into a dictionary automatically."""
        return vars(self)

    def adjust_winstreak(self, lose: bool = False):
        if not lose and self.winstreak < 0:
            self.winstreak = 1
        elif not lose and self.winstreak > 0:
            self.winstreak += 1
        elif lose and self.winstreak > 0:
            self.winstreak = 0
        elif lose and self.winstreak < 0:
            self.winstreak += -1

# player and dealer classes
class Player:
    def __init__(self, money: float, profit: float, stats: Stats, frame = None):
        self.frame = frame
        self.cards = []
        self.__money = money
        self.__profit = profit
        self.__session_profit = 0
        self.bet = 0
        self.original_bet = 0
        self.double = False

        self.stats = stats

    def get_score(self):
        return calculate_score(self.cards)

    def adjust_profit(self, value):
        self.__profit += value
        self.__session_profit += value

    def set_money(self, value: float):
        self.__money = value

    def adjust_money(self, value):
        value = round(value, 2)
        self.__money += value
        self.adjust_profit(value)

    def get_money(self):
        return self.__money

    def get_profit(self, session: bool = False):
        if not session: return self.__profit
        else: return self.__session_profit

class Dealer:
    def __init__(self, frame = None):
        self.frame = frame
        self.cards = []

    def get_score(self, dealers_first: bool = False):
        if dealers_first: return card_value(self.cards[0])
        else: return calculate_score(self.cards)


# settings
class Settings:
    def __init__(self, cooldown: int = 750, deck_amount: int = 6, dealer_stop: int = 17, credit_card_debt = 1000, **kwargs):
        self.cooldown = cooldown
        self.deck_amount = deck_amount
        self.dealer_stop = dealer_stop
        self.credit_card_debt = credit_card_debt

    def to_dict(self):
        """Helper to turn this object into a dictionary automatically."""
        return vars(self)

# types of wins enum
class ResultType(Enum):
    NONE = "NONE"
    DEALER_HIGHER = "DEALER_HIGHER"
    PLAYER_HIGHER = "PLAYER_HIGHER"
    DEALER_BUST = "DEALER_BUST"
    PLAYER_BUST = "PLAYER_BUST"
    PUSH = "PUSH"
    PUSH_BLACKJACK = "PUSH_BLACKJACK"
    DEALER_BLACKJACK = "DEALER_BLACKJACK"
    PLAYER_BLACKJACK = "PLAYER_BLACKJACK"

# end-of-game result class for easy saving and checking
class Result:
    def __init__(self, player: Player, dealer: Dealer, win_type: ResultType = ResultType.NONE):
        self.player_cards = player.cards
        self.dealer_cards = dealer.cards
        self.bet = player.bet
        self.is_double_down = player.original_bet != player.bet
        self.player_score = player.get_score()
        self.dealer_score = dealer.get_score()
        self.__win_type = win_type
        self.__result_string = self.set_result_string()

    def set_win_type(self, win_type: ResultType):
        self.__win_type = win_type
        self.set_result_string()
    def get_win_type(self) -> ResultType:
        return self.__win_type
    def get_result_string(self) -> str:
        return self.__result_string

    def set_result_string(self) -> str:
        match self.__win_type:
            case ResultType.PLAYER_BUST: return f"You are bust! You lose ${self.bet}!"
            case ResultType.DEALER_BUST: return f"Dealers bust! You win ${self.bet*2}!"
            case ResultType.PUSH: return f"Push! You get ${self.bet} back!"
            case ResultType.PLAYER_HIGHER: return f"Your score is higher! You win ${self.bet*2}!"
            case ResultType.DEALER_HIGHER: return f"Your score is lower! You lose ${self.bet}!"
            case ResultType.PUSH_BLACKJACK: return f"Both have Blackjack! Push! You get ${self.bet} back"
            case ResultType.PLAYER_BLACKJACK: return f"Blackjack! You win ${int(self.bet + (self.bet * 1.5))}!"
            case ResultType.DEALER_BLACKJACK: return f"Dealer has Blackjack! You lose ${self.bet}!"
        return ""

    def to_dict(self):
        """Helper to turn this object into a dictionary automatically."""
        return {
            "player_cards": self.player_cards,
            "dealer_cards": self.dealer_cards,
            "player_score": self.player_score,
            "dealer_score": self.dealer_score,
            "bet": self.bet,
            "double_down": self.is_double_down,
            "win_type": self.get_win_type().name,
            "message": self.get_result_string()
        }