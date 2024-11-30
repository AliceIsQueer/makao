from enum import IntEnum
from colorama import Fore, Style


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
    """
    Class Card. Contains attributes:

    :param suit: The card's suit
    :type suit: int

    :param value: Card's value from Two to Ace
    :type value: int
    """
    def __init__(self, suit: int, value: int):
        """
        Initialises the card class. Throws error if the card given is invalid
        """
        values = [value for value in Suits]
        if suit not in values:
            raise InvalidSuitError()
        self._suit = suit

        if value > 14 or value < 1:
            raise ValueNotInRangeError()
        self._value = value

    @property
    def suit(self) -> int:
        return self._suit

    @property
    def value(self) -> int:
        return self._value

    def can_put_card(self, other: 'Card') -> bool:
        """
        Returns True if this card can be put on the card given.
        Returns False otherwise
        Follows the rules of the game
        """
        if (other.value == self.value or other.suit == self.suit
           or self.value == 12 or other.value == 12):
            return True
        return False

    def __str__(self) -> str:
        """
        Returns the name of the card
        """
        names = ['2', '3', '4', '5', '6', '7', '8',
                 '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['\u2660', '\u2666', '\u2663', '\u2665']

        color = (Fore.RED if (self.suit) in (Suits.DIAMONDS, Suits.HEARTS)
                 else Fore.BLACK)
        return (f'{names[self.value - 2]}{color + suits[self.suit - 1]}'
                + Style.RESET_ALL)

    def __eq__(self, other: 'Card'):
        return self.suit == other.suit and self.value == other.value

    # def trigger_card_effect(self, next_player: 'Player'):
    #     pass
