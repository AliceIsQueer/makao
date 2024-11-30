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
        for index, card in enumerate(self.hand):
            if self.allowed_cards != []:
                if self.allowed_cards == card.value:
                    return index
            else:
                if (card.can_put_card(card_stack.top_card)):
                    return index
        return len(self.hand)
