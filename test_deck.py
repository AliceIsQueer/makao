from deck import Deck


def test_deck_init():
    deck = Deck()
    assert len(deck.cards) == 52


def test_deck_draw_card():
    deck = Deck()
    assert len(deck.cards) == 52
    deck.draw_card()
    assert len(deck.cards) == 51


def test_deck_refresh():
    deck = Deck()
    assert len(deck.cards) == 52
    deck.draw_card()
    assert len(deck.cards) == 51
    deck.refresh_deck()
    assert len(deck.cards) == 52
