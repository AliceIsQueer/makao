from game import Game


def test_game_init():
    game = Game("Alice", 2)
    assert len(game.players) == 3


def test_game_turn_counter():
    game = Game("Alice", 2)
    assert game.get_current_player().name == "Alice"
    game.increment_turn()
    assert game.get_current_player().name == "Player1"
    game.increment_turn()
    assert game.get_current_player().name == "Player2"
    game.increment_turn()
    assert game.get_current_player().name == "Alice"
    game.increment_turn()

