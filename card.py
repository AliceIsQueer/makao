from enum import IntEnum


class InvalidSuitError(Exception):
    def __init__(self):
        super().__init__("This is not a valid card suite")


class ValueNotInRangeError(Exception):
    def __init__(self):
        super().__init__("A card's value has to be between 1 and 13")


class Suits(IntEnum):
    SPADES = 1
    DIAMONDS = 2
    CLUBS = 3
    HEARTS = 4


class Card:
    def __init__(self, suit: int, value: int):
        values = [value for value in Suits]
        if suit not in values:
            raise InvalidSuitError()
        self._suit = suit

        if value > 14 or value < 1:
            raise ValueNotInRangeError()
        self._value = value

    @property
    def suit(self):
        return self._suit

    @property
    def value(self):
        return self._value

    def can_put_card(self, other: 'Card'):
        if (other.value == self.value or other.suit == self.suit
           or self.value == 12):
            return True
        return False

    def __str__(self):
        names = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
                 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']

        return f'{names[self.value - 1]} of {suits[self.suit - 1]}'
