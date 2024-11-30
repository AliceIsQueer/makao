from player import Player
from card import Card
from typing import List, Optional
from card_stack import CardStack
from random import random


class Opponent(Player):
    """
    Class Opponent. Inherits from Player.
    """
    def __init__(self, name: str, cards: Optional[List[Card]] = None):
        """Initialises the Opponent class"""
        super().__init__(name, cards)

    def get_optimal_card(self, card_stack: 'CardStack') -> int:
        """
        Returns the index of a card to be played by the opponent
        Returns -1 if the opponent should skip their turn
        """
        ans = len(self.hand)
        for index, card in enumerate(self.hand):
            if self.allowed_cards != []:
                if card.value in self.allowed_cards:
                    ans = index
            else:
                if (card_stack.is_valid_combo([card])):
                    ans = index
        if ans != len(self.hand) and len(self.hand) == 2:
            if random() > 0.5:
                self.set_said_makao()
        return ans

    def get_optimal_suit(self) -> int:
        """Returns the optimal suit after the Ace special effect"""
        suits_in_hand = [0]*4
        for card in self.hand:
            suit = card.suit
            suits_in_hand[suit - 1] += 1

        return suits_in_hand.index(max(suits_in_hand)) + 1

    def get_optimal_value(self) -> int:
        """Returns the optimal card value after the Jack interction"""
        cards_in_hand = [0]*13
        for card in self.hand:
            value = card.value
            cards_in_hand[value-1] += 1

        return cards_in_hand[4:10].index(max(cards_in_hand[4:10])) + 5
