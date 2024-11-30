from typing import List, Optional
from card import Card
from player import Player


class CardStack:
    """
    Class CardStack. Contains attributes:

    :param cards: The cards on the card pile
    :type cards: List['Card']
    """
    def __init__(self, cards: Optional[List['Card']] = None):
        """Initialises the CardStack class"""
        if not cards:
            self._cards = []
        else:
            self._cards = cards

    @property
    def cards(self) -> List['Card']:
        return self._cards

    @property
    def top_card(self) -> 'Card':
        """Returns the card at the top of the card stack"""
        return self.cards[-1]

    def __str__(self):
        """Gives a brief description of the card on top of the stack"""
        return f'The card at the top is {self.top_card}'

    def add_card_on_top(self, card: 'Card'):
        """Adds a card on top of the card stack"""
        self._cards.append(card)

    def trigger_top_effect(self, next_player: 'Player', prev_player: 'Player'):
        pass
