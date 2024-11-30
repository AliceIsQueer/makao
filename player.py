from card import Card
from typing import List, Optional


class WrongCardIndexError(Exception):
    def __init__(self):
        super().__init__("The given card index is out of range")


class Player:
    """
    Class Player. Contains attributes:

    :param name: The player's name, used for aesthetic purposes
    :type name: str

    :param hand: Player's hand of cards
    :type hand: List[Card]

    :param blocked: Whether or not the player will take part in their next turn
    :type blocked: boolean
    """
    def __init__(self, name: str, cards: Optional[List[Card]] = None):
        """Initialises the player class"""
        if not cards:
            self._hand = []
        else:
            self._hand = cards

        self._name = name
        self._blocked = False

    @property
    def hand(self) -> List[Card]:
        return self._hand

    @property
    def name(self):
        return self._name

    @property
    def blocked(self):
        return self._blocked

    def add_card(self, card: 'Card') -> None:
        """Adds a card to the player's hand"""
        self._hand.append(card)

    def remove_card(self, card_index: int) -> 'Card':
        """
        Removes a card from the player's hand
        Throws error if given an invalid index
        """
        try:
            return self._hand.pop(card_index)
        except IndexError:
            raise WrongCardIndexError()

    def block_next_turn(self):
        self._blocked = True

    def unblock(self):
        self._blocked = False

    def get_hand_description(self):
        card_list = ''
        for index, card in enumerate(self.hand):
            card_list += f'{index + 1} - {card} \n'
        return f'Your hand consists of: \n{card_list}'
