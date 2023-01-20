from player import Player
from card import Card
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
        self.set_said_makao()
        for index, card in enumerate(self.hand):
            if self.allowed_cards != []:
                if card.value in self.allowed_cards:
                    return index
            else:
                if (card_stack.is_valid_combo([card])):
                    return index
        return len(self.hand)

    def get_optimal_suit(self):
        suits_in_hand = [0]*4
        for card in self.hand:
            suit = card.suit
            suits_in_hand[suit - 1] += 1

        return suits_in_hand.index(max(suits_in_hand)) + 1

    def get_optimal_value(self):
        cards_in_hand = [0]*13
        for card in self.hand:
            value = card.value
            cards_in_hand[value-1] += 1

        return cards_in_hand[4:10].index(max(cards_in_hand[4:10])) + 5
