from card import Card, Suits
from typing import List
import random


class Deck:
    """
    Class Deck. Contains attributes:

    :param cards: Cards that are currently in the deck. Starts with 52 cards
    :type cards: List[Card]
    """
    def __init__(self):
        """Initialises the Deck Class with 52 cards in it"""
        self._cards = []
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
        return self._cards.pop()

    def refresh_deck(self) -> None:
        """Resets the deck's cards to their base state"""
        self._cards = []
        for suit in Suits:
            for value in range(1, 14):
                self._cards.append(Card(suit, value))
