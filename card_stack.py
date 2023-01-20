from typing import List, Optional
from card import Card, Suits
from player import Player, Status


class KingOfSpadesException(Exception):
    def __init__(self):
        super().__init__('Someone has played the king of spades')


class AceException(Exception):
    def __init__(self):
        super().__init__('Someone has played an ace')


class JackException(Exception):
    def __init__(self):
        super().__init__('Someone has played a jack')


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

        self._forced_suit = None
        self._forced_value = None

    @property
    def cards(self) -> List['Card']:
        return self._cards

    @property
    def forced_suit(self):
        return self._forced_suit

    @property
    def forced_value(self):
        return self._forced_value

    @property
    def top_card(self) -> 'Card':
        """Returns the card at the top of the card stack"""
        return self.cards[-1]

    def set_forced_suit(self, suit):
        self._forced_suit = suit

    def reset_forced_suit(self):
        self._forced_suit = None

    def set_forced_value(self, value):
        self._forced_value = value

    def reset_forced_value(self):
        self._forced_value = None

    def is_valid_combo(self, cards: List['Card']) -> bool:
        for index, card in enumerate(cards):
            if index == 0:
                if self.forced_suit is None and self.forced_value is None:
                    if not card.can_put_card(self.top_card):
                        return False
                else:
                    if self.forced_suit is not None:
                        if card.value == self.top_card.value:
                            continue
                        if card.suit != self.forced_suit:
                            return False
                    else:
                        if not (card.value == self.forced_value or
                                (card.value == self.top_card.value and
                                 card.value == 11)):
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
            if self.forced_suit is not None:
                self.reset_forced_suit()
            self.trigger_top_effect(prev_player, next_player, all_players)

    def trigger_top_effect(self, prev_player: 'Player',
                           next_player: 'Player', all_players: List['Player']):
        """Triggers the effect based on the rules of makao"""
        if prev_player is None or next_player is None:
            return

        card = self.top_card

        if card.value == 2 or card.value == 3:
            next_player.set_status_effect(Status.DRAW2OR3)
            next_player.increase_cards_to_draw(card.value)
        elif card.value == 4:
            next_player.set_status_effect(Status.BLOCKED)
            next_player.increase_block()
        elif card.value == 11:
            for player in all_players:
                if not player.won:
                    player.set_status_effect(Status.FORCESUIT)
            raise JackException
        elif card.value == 13:
            if card.suit == Suits.SPADES:
                prev_player.set_status_effect(Status.DRAW5)
                prev_player.increase_cards_to_draw(5)
                raise KingOfSpadesException
            elif card.suit == Suits.HEARTS:
                next_player.set_status_effect(Status.DRAW5)
                next_player.increase_cards_to_draw(5)
        elif card.value == 1:
            raise AceException
