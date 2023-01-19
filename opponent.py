from player import Player
from card import Card, Suits
from typing import List, Optional
from card_stack import CardStack


class Opponent(Player):
    def __init__(self, name: str, cards: Optional[List[Card]] = None):
        super().__init__(name, cards)

    def get_optimal_card(self, card_stack: 'CardStack') -> int:
        """
        Returns the index of a card to be played by the opponent
        Returns -1 if the opponent should skip their turn
        """
        for index, card in enumerate(self.hand):
            if self.allowed_cards != []:
                if self.allowed_cards == card.value:
                    return index
            else:
                if (card_stack.is_valid_combo([card])):
                    return index
        return len(self.hand)

    def get_optimal_suit(self):
        suits_in_hand = {}
        for suit in Suits:
            suits_in_hand[suit] = 0

        for card in self.hand:
            suit = card.suit
            suits_in_hand[suit] += 1

        suits_to_list = [suits_in_hand[key] for key in suits_in_hand] 
        return suits_to_list[suits_to_list.index(max(suits_to_list))] + 1