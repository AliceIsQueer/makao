from card_stack import CardStack
from card import Card, Suits
from player import Player, Status


def test_card_stack_init():
    stack = CardStack()
    assert len(stack.cards) == 0


def test_card_stack_adds_card():
    stack = CardStack()
    two_of_spades = Card(Suits.SPADES, 2)
    stack.add_cards_on_top([two_of_spades])
    assert len(stack.cards) == 1
    assert two_of_spades in stack.cards
    assert stack.top_card == two_of_spades


def test_card_stack_str():
    stack = CardStack()
    two_of_spades = Card(Suits.SPADES, 2)
    stack.add_cards_on_top([two_of_spades])
    assert str(stack) == f'The card at the top is {two_of_spades}'


def test_card_stack_block():
    stack = CardStack()
    four_of_hearts = Card(Suits.HEARTS, 4)
    next_player = Player([])
    prev_player = Player([])
    all_players = [next_player, prev_player]
    stack.add_cards_on_top([four_of_hearts], prev_player,
                           next_player, all_players)
    assert next_player.status_effect == Status.BLOCKED


def test_card_stack_add2():
    stack = CardStack()
    two_of_hearts = Card(Suits.HEARTS, 2)
    next_player = Player([])
    prev_player = Player([])
    all_players = [next_player, prev_player]
    stack.add_cards_on_top([two_of_hearts], prev_player,
                           next_player, all_players)
    assert next_player.status_effect == Status.DRAW2OR3


def test_card_stack_add3():
    stack = CardStack()
    three_of_hearts = Card(Suits.HEARTS, 3)
    next_player = Player([])
    prev_player = Player([])
    all_players = [next_player, prev_player]
    stack.add_cards_on_top([three_of_hearts], prev_player,
                           next_player, all_players)
    assert next_player.status_effect == Status.DRAW2OR3


def test_card_stack_add5_prev():
    stack = CardStack()
    king_of_spades = Card(Suits.SPADES, 13)
    next_player = Player([])
    prev_player = Player([])
    all_players = [next_player, prev_player]
    stack.add_cards_on_top([king_of_spades], prev_player,
                           next_player, all_players)
    assert prev_player.status_effect == Status.DRAW5


def test_card_stack_add5_next():
    stack = CardStack()
    king_of_hearts = Card(Suits.HEARTS, 13)
    next_player = Player([])
    prev_player = Player([])
    all_players = [next_player, prev_player]
    stack.add_cards_on_top([king_of_hearts], prev_player,
                           next_player, all_players)
    assert next_player.status_effect == Status.DRAW5
