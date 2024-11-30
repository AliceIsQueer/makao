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
    assert len(alice.cards) == 1
    assert two_of_spades in alice.cards


def test_player_remove_card():
    alice = Player("Alice")
    two_of_spades = Card(Suits.SPADES, 2)
    queen_of_hearts = Card(Suits.HEARTS, 12)
    alice.add_card(two_of_spades)
    alice.add_card(queen_of_hearts)
    assert len(alice.cards) == 2
    assert two_of_spades in alice.cards
    assert queen_of_hearts in alice.cards
    alice.remove_card(1)
    assert len(alice.cards) == 1
    assert two_of_spades in alice.cards
    assert queen_of_hearts not in alice.cards


def test_player_remove_card_wrong_index():
    alice = Player("Alice")
    two_of_spades = Card(Suits.SPADES, 2)
    alice.add_card(two_of_spades)
    assert len(alice.cards) == 1
    assert two_of_spades in alice.cards
    with pytest.raises(WrongCardIndexError):
        alice.remove_card(1)
