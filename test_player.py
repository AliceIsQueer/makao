from player import Player, WrongCardIndexError
import pytest
from card import Card, Suits


def test_player_init():
    alice = Player("Alice")
    assert alice.name == "Alice"


def test_player_add_card():
    alice = Player("Alice")
    two_of_spades = Card(Suits.SPADES, 2)
    alice.add_card(two_of_spades)
    assert len(alice.hand) == 1
    assert two_of_spades in alice.hand


def test_player_remove_card():
    alice = Player("Alice")
    two_of_spades = Card(Suits.SPADES, 2)
    queen_of_hearts = Card(Suits.HEARTS, 12)
    alice.add_card(two_of_spades)
    alice.add_card(queen_of_hearts)
    assert len(alice.hand) == 2
    assert two_of_spades in alice.hand
    assert queen_of_hearts in alice.hand
    alice.remove_cards([1])
    assert len(alice.hand) == 1
    assert two_of_spades in alice.hand
    assert queen_of_hearts not in alice.hand


def test_player_remove_card_wrong_index():
    alice = Player("Alice")
    two_of_spades = Card(Suits.SPADES, 2)
    alice.add_card(two_of_spades)
    assert len(alice.hand) == 1
    assert two_of_spades in alice.hand
    with pytest.raises(WrongCardIndexError):
        alice.remove_cards([1])


def test_player_hand_description():
    two_of_spades = Card(Suits.SPADES, 2)
    queen_of_hearts = Card(Suits.HEARTS, 12)
    alice = Player("Alice", [two_of_spades, queen_of_hearts])
    assert alice.get_hand_description() == f'Your hand consists of: \n1 - {str(two_of_spades)} \n2 - {str(queen_of_hearts)} \n' # NOQA
