from card import Card
from typing import List, Optional
from enum import IntEnum


class WrongCardIndexError(Exception):
    def __init__(self):
        super().__init__("The given card index is out of range")


class Status(IntEnum):
    NOEFFECT = 1
    DRAW2OR3 = 2
    BLOCKED = 3
    FORCESUIT = 4
    DRAW5 = 5


class Player:
    """
    Class Player. Contains attributes:

    :param name: The player's name, used for aesthetic purposes
    :type name: str

    :param hand: Player's hand of cards
    :type hand: List[Card]

    :param total_blocked_turns: The amount of turns the player will blocked
    :type total_blocked_turns: int
    """
    def __init__(self, name: str, cards: Optional[List[Card]] = None):
        """Initialises the player class"""
        if not cards:
            self._hand = []
        else:
            self._hand = cards

        self._name = name
        self._total_blocked_turns = 0
        self._blocked_turns = 0
        self._cards_to_draw = 0
        self._status_effect = Status.NOEFFECT
        self._allowed_cards = []

    @property
    def hand(self) -> List[Card]:
        return self._hand

    @property
    def name(self):
        return self._name

    @property
    def total_blocked_turns(self):
        return self._total_blocked_turns

    @property
    def blocked_turns(self):
        return self._blocked_turns

    @property
    def status_effect(self):
        return self._status_effect

    @property
    def allowed_cards(self):
        return self._allowed_cards

    @property
    def cards_to_draw(self):
        return self._cards_to_draw

    def add_card(self, card: 'Card') -> None:
        """Adds a card to the player's hand"""
        self._hand.append(card)

    def remove_cards(self, indexes: List[int]) -> 'Card':
        """
        Removes cards from the player's hand
        Throws error if given an invalid index
        """
        new_hand = []
        removed_cards = []

        for index in indexes:
            if index > len(self.hand)-1 or index < 0:
                raise WrongCardIndexError

        for index, card in enumerate(self.hand):
            if index not in indexes:
                new_hand.append(card)
            else:
                removed_cards.append(card)

        self._hand = new_hand
        return removed_cards
        # try:
        #     return self._hand.pop(card_index)
        # except IndexError:
        #     raise WrongCardIndexError()

    def increase_block(self):
        self._total_blocked_turns += 1
        self._blocked_turns = self._total_blocked_turns

    def decrement_block(self):
        self._blocked_turns -= 1
        if self.blocked_turns == 0:
            self._total_blocked_turns = 0
            self._status_effect = Status.NOEFFECT
            self._allowed_cards = []

    def increase_cards_to_draw(self, num):
        self._cards_to_draw += num

    def reset_cards_to_draw(self):
        self._cards_to_draw = 0
        self._status_effect = Status.NOEFFECT
        self._allowed_cards = []

    def get_hand_description(self):
        card_list = ''
        for index, card in enumerate(self.hand):
            card_list += f'{index + 1} - {card} \n'
        return f'Your hand consists of: \n{card_list}'

    def set_status_effect(self, effect: int) -> None:
        self._status_effect = effect

    def remove_status_effect(self) -> List[int]:
        self._status_effect = Status.NOEFFECT
        self._total_blocked_turns = 0
        self._blocked_turns = 0
        self._cards_to_draw = 0

    def transfer_effect(self, other: 'Player'):
        other.set_status_effect(self.status_effect)
        other._total_blocked_turns = self._total_blocked_turns
        other._blocked_turns = self._blocked_turns
        other._cards_to_draw = self._cards_to_draw
        self.remove_status_effect()

    def set_allowed_cards(self, card_values):
        self._allowed_cards = card_values

    def clear_allowed_card(self):
        self._allowed_cards.clear()

    def __str__(self):
        return self.name
