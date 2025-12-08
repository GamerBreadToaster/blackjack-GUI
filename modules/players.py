from modules.score_calc import calculate_score, card_value
from modules.info_getter import set_info

# player and dealer classes
class Player:
    def __init__(self, money: float, profit: float, frame = None):
        self.frame = frame
        self.cards = []
        self.__money = money
        self.__profit = profit
        self.bet = 0
        self.double = False

    def get_score(self):
        return calculate_score(self.cards)

    def adjust_profit(self, value):
        self.__profit += value

    def set_money(self, value: float):
        self.__money = value

    def adjust_money(self, value):
        self.__money += value
        self.adjust_profit(value)
        set_info(self.__money, self.__profit)
        # automatically save money to save on using repeating code

    def get_money(self):
        return self.__money

    def get_profit(self):
        return self.__profit

class Dealer:
    def __init__(self, frame = None):
        self.frame = frame
        self.cards = []

    def get_score(self, dealers_first: bool = False):
        if dealers_first: return card_value(self.cards[0])
        else: return calculate_score(self.cards)