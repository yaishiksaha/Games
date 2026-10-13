
from game import ChopsticksGame


def test_self_attack():
    game = ChopsticksGame()
    game.hands[1] = [2, 2]

    assert game.attack(0, 1, 1) is True
    assert game.hands[1] == [2, 4]


def test_increment_with_eliminated_hand():
    game = ChopsticksGame()
    game.hands[1] = [0, 2]

    assert game.increment(1) is True
    assert game.hands[1] == [0, 3]


def test_increment_from_one():
    game = ChopsticksGame()
    game.hands[1] = [1, 2]

    assert game.increment(0) is True
    assert game.hands[1] == [2, 2]


def test_increment_eliminates_hand():
    game = ChopsticksGame()
    game.hands[1] = [4, 2]

    assert game.increment(0) is True
    assert game.hands[1] == [0, 2]


def test_split():
    game = ChopsticksGame()
    game.hands[1] = [0, 2]

    assert game.split() is True
    assert game.hands[1] == [1, 1]
    assert game.split_count[1] == 1


def test_invalid_split():
    game = ChopsticksGame()
    game.hands[1] = [2, 4]

    assert game.split() is False
    assert game.hands[1] == [2, 4]


def test_winner():
    game = ChopsticksGame()
    game.hands[2] = [0, 0]

    assert game.check_winner() == 1

def test_split_limit():
    game = ChopsticksGame()

    # Use all three permitted splits.
    for _ in range(3):
        game.hands[1] = [2, 2]
        assert game.split() is True

    # A fourth split must fail.
    game.hands[1] = [2, 2]
    assert game.split() is False
    assert game.split_count[1] == 3


def test_attack_eliminates_hand():
    game = ChopsticksGame()

    game.hands[1] = [2, 1]
    game.hands[2] = [3, 1]

    # Player 1 attacks Player 2's left hand.
    assert game.attack(0, 2, 0) is True
    assert game.hands[2] == [0, 1]


if __name__ == "__main__":
    test_self_attack()
    test_increment_with_eliminated_hand()
    test_increment_from_one()
    test_increment_eliminates_hand()
    test_split()
    test_invalid_split()
    test_winner()
    test_split_limit()
    test_attack_eliminates_hand()

    print("All tests passed!")
