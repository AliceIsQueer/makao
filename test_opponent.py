from opponent import Opponent
from card import Card, Suits


def test_opponent_get_optimal_suit_1():
    hand = []
    for val in range(3, 6):
        hand.append(Card(Suits.SPADES, val))
    for val in range(3, 5):
        hand.append(Card(Suits.HEARTS, val))
    opp = Opponent('Bob', hand)

    assert opp.get_optimal_suit() == Suits.SPADES


def test_opponent_get_optimal_suit_2():
    hand = []
    for val in range(3, 6):
        hand.append(Card(Suits.SPADES, val))
    for val in range(3, 6):
        hand.append(Card(Suits.HEARTS, val))
    opp = Opponent('Bob', hand)

    assert opp.get_optimal_suit() == Suits.SPADES
