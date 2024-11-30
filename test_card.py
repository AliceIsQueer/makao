from card import Card, Suits, InvalidSuitError, ValueNotInRangeError
import pytest


def test_card_init():
    two_of_spades = Card(Suits.SPADES, 1)
    assert two_of_spades.suit == Suits.SPADES
    assert two_of_spades.value == 1


def test_card_init_invalid_suit():
    with pytest.raises(InvalidSuitError):
        Card(5, 1)


def test_card_init_invaid_value():
    with pytest.raises(ValueNotInRangeError):
        Card(Suits.SPADES, 15)


def test_card_name():
    two_of_spades = Card(Suits.SPADES, 2)
    assert str(two_of_spades) == 'Two of Spades'
