from typing import List, Optional
from card import Card, Suits
from player import Player, Status


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

    def is_valid_combo(self, cards: List['Card']) -> bool:
        for index, card in enumerate(cards):
            if index == 0:
                if not card.can_put_card(self.top_card):
                    return False
            else:
                if not card.can_put_card(cards[index-1]):
                    return False

        return True

    def __str__(self):
        """Gives a brief description of the card on top of the stack"""
        return f'The card at the top is {self.top_card}'

    def remove_bottom_cards(self):
        removed = self.cards[0:-1]
        self._cards = self.cards[-1:]
        return removed

    def add_cards_on_top(self, cards: List['Card'],
                         prev_player: 'Player' = None,
                         next_player: 'Player' = None,
                         all_players: List['Player'] = None):
        """Adds a card on top of the card stack"""

        for card in cards:
            self._cards.append(card)
            self.trigger_top_effect(prev_player, next_player, all_players)

    def trigger_top_effect(self, prev_player: 'Player',
                           next_player: 'Player', all_players: List['Player']):
        """Triggers the effect based on the rules of makao"""
        if prev_player is None or next_player is None:
            return

        card = self.top_card

        if card.value == 2 or card.value == 3:
            next_player.set_status_effect(Status.DRAW2OR3)
        elif card.value == 4:
            next_player.set_status_effect(Status.BLOCKED)
            next_player.increase_block()
        elif card.value == 11:
            for player in all_players:
                player.set_status_effect(Status.FORCESUIT)
        elif card.value == 13:
            if card.suit == Suits.SPADES:
                prev_player.set_status_effect(Status.DRAW5)
            elif card.suit == Suits.HEARTS:
                next_player.set_status_effect(Status.DRAW5)
