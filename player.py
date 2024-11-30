from card import Card
from typing import List, Optional


class WrongCardIndexError(Exception):
    def __init__(self):
        super().__init__("The given card index is out of range")


class Player:
    def __init__(self, name: str, cards: Optional[List[Card]] = None):
        if not cards:
            self._cards = []
        else:
            self._cards = cards

        self._name = name

    @property
    def cards(self) -> List[Card]:
        return self._cards

    @property
    def name(self):
        return self._name

    def add_card(self, card: 'Card') -> None:
        self._cards.append(card)

    def remove_card(self, card_index: int) -> 'Card':
        try:
            return self._cards.pop(card_index)
        except IndexError:
            raise WrongCardIndexError()
