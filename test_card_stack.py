from card_stack import CardStack
from card import Card, Suits


def test_card_stack_init():
    stack = CardStack()
    assert len(stack.cards) == 0


def test_card_stack_add_card():
    stack = CardStack()
    two_of_spades = Card(Suits.SPADES, 2)
    stack.add_card_on_top(two_of_spades)
    assert len(stack.cards) == 1
    assert two_of_spades in stack.cards
    assert stack.top_card == two_of_spades


def test_card_stack_str():
    stack = CardStack()
    two_of_spades = Card(Suits.SPADES, 2)
    stack.add_card_on_top(two_of_spades)
    assert str(stack) == 'The card at the top is Two of Spades'
