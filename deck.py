from card import Card, Suits
from card_stack import CardStack
from typing import List
import random


class EmptyDeckError(Exception):
    def __init__(self):
        super().__init__("The deck is empty.")


class Deck:
    """
    Class Deck. Contains attributes:

    :param cards: Cards that are currently in the deck. Starts with 52 cards
    :type cards: List[Card]

    :param card_stack: The stack that is bound to this deck
    :type card_stack: 'CardStack'
    """
    def __init__(self, card_stack: CardStack) -> None:
        """Initialises the Deck Class with 52 cards in it"""
        self._cards = []
        self._card_stack = card_stack
        for suit in Suits:
            for value in range(1, 14):
                self._cards.append(Card(suit, value))

    @property
    def cards(self) -> List[Card]:
        return self._cards

    def shuffle_deck(self) -> None:
        """Shuffles the deck randomly"""
        random.shuffle(self._cards)

    def draw_card(self) -> 'Card':
        """Removes the card from top of the deck and returns it"""
        if len(self._cards) == 0:
            self._cards = self._card_stack.remove_bottom_cards()
            self.shuffle_deck()
        if len(self._cards) == 0:
            raise EmptyDeckError
        else:
            return self._cards.pop()

    def refresh_deck(self) -> None:
        """Resets the deck's cards to their base state"""
        self._cards = []
        for suit in Suits:
            for value in range(1, 14):
                self._cards.append(Card(suit, value))
