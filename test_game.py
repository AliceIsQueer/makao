from game import Game, InvalidOppNumError 
import pytest


def test_game_init(monkeypatch):
    monkeypatch.setattr(Game, 'handle_turn', lambda self: None)
    game = Game("Alice", 2)
    assert len(game.players) == 3


def test_game_init_wrong_opp_num(monkeypatch):
    monkeypatch.setattr(Game, 'handle_turn', lambda self: None)
    with pytest.raises(InvalidOppNumError):
        Game('Alice', 4)


def test_game_turn_counter(monkeypatch):
    monkeypatch.setattr(Game, 'handle_turn', lambda self: None)
    game = Game("Alice", 2)
    assert game.get_current_player().name == "Alice"
    game.increment_turn()
    assert game.get_current_player().name == "Player1"
    game.increment_turn()
    assert game.get_current_player().name == "Player2"
    game.increment_turn()
    assert game.get_current_player().name == "Alice"
    game.increment_turn()


def test_game_next_player(monkeypatch):
    monkeypatch.setattr(Game, 'handle_turn', lambda self: None)
    game = Game('Alice', 2)
    alice, opp1, opp2 = game.players
    assert game.get_current_player() == alice
    assert game.right_of_player(alice) == opp1
    assert game.left_of_player(alice) == opp2
    assert game.right_of_player(opp1) == opp2
    assert game.left_of_player(opp1) == alice
    assert game.right_of_player(opp2) == alice
    assert game.left_of_player(opp2) == opp1
