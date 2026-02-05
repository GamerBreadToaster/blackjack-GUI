from modules.score_calc import calculate_score, card_value

# player and dealer classes
class Player:
    def __init__(self, money: float, profit: float, frame = None):
        self.frame = frame
        self.cards = []
        self.__money = money
        self.__profit = profit
        self.__session_profit = 0
        self.bet = 0
        self.original_bet = 0
        self.double = False

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

class Settings:
    def __init__(self, cooldown: int, amount: int):
        self.cooldown = cooldown
        self.deck_amount = amount