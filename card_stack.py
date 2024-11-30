from typing import List, Optional
from card import Card


class CardStack:

    def __init__(self, cards: Optional[List['Card']] = None):
        if not cards:
            self._cards = []
        else:
            self._cards = cards

    @property
    def cards(self) -> List['Card']:
        return self._cards

    def top_card(self) -> 'Card':
        return self.cards[-1]

    def add_card_on_top(self, card: 'Card'):
        self._cards.append(card)
