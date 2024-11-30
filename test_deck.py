from deck import Deck
from card_stack import CardStack


def test_deck_init():
    stack = CardStack()
    deck = Deck(stack)
    assert len(deck.cards) == 52


def test_deck_draw_card():
    stack = CardStack()
    deck = Deck(stack)
    assert len(deck.cards) == 52
    deck.draw_card()
    assert len(deck.cards) == 51


def test_deck_refresh():
    stack = CardStack()
    deck = Deck(stack)
    assert len(deck.cards) == 52
    deck.draw_card()
    assert len(deck.cards) == 51
    deck.refresh_deck()
    assert len(deck.cards) == 52
