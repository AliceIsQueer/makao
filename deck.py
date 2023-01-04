from card import Card, Suits
import random


class Deck:
    def __init__(self):
        self._cards = []
        for suit in Suits:
            for value in range(1, 14):
                self._cards.append(Card(suit, value))

    @property
    def cards(self):
        return self._cards

    def shuffle_deck(self):
        random.shuffle(self._cards)

    def draw_card(self):
        return self._cards.pop()

    def refresh_deck(self):
        self._cards = []
        for suit in Suits:
            for value in range(1, 14):
                self._cards.append(Card(suit, value))
