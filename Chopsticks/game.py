
class ChopsticksGame:
    def __init__(self):
        self.hands = {
            1: [1, 1],
            2: [1, 1]
        }

        self.current_player = 1
        self.split_count = {
            1: 0,
            2: 0
        }

    def attack(self, attacker_hand, target_player, target_hand):
        """Add an attacking hand's value to a target hand."""

        player = self.current_player

        # Hand indices: 0 = left, 1 = right.
        if attacker_hand not in (0, 1):
            return False

        if target_hand not in (0, 1):
            return False

        if target_player not in (1, 2):
            return False

        attacking_value = self.hands[player][attacker_hand]
        target_value = self.hands[target_player][target_hand]

        # Cannot attack with an eliminated hand.
        if attacking_value == 0:
            return False

        # Cannot attack an eliminated hand.
        if target_value == 0:
            return False

        # An attack cannot target your own attacking hand.
        if player == target_player and attacker_hand == target_hand:
            return False

        new_value = attacking_value + target_value

        # Five or more eliminates the target hand.
        if new_value >= 5:
            self.hands[target_player][target_hand] = 0
        else:
            self.hands[target_player][target_hand] = new_value

        return True

    def increment(self, hand_index):
        """Increase one of your active hands by one."""

        player = self.current_player

        if hand_index not in (0, 1):
            return False

        if self.hands[player][hand_index] == 0:
            return False

        new_value = self.hands[player][hand_index] + 1

        if new_value >= 5:
            self.hands[player][hand_index] = 0
        else:
            self.hands[player][hand_index] = new_value

        return True

    def split(self):
        """Split only the four permitted configurations."""

        player = self.current_player
        left, right = self.hands[player]

        split_results = {
            (0, 2): [1, 1],
            (2, 0): [1, 1],
            (0, 4): [2, 2],
            (4, 0): [2, 2],
            (2, 2): [1, 1],
            (4, 4): [2, 2]
        }

        # Check the split limit.
        if self.split_count[player] >= 3:
            return False

        # Check whether the current configuration is permitted.
        configuration = (left, right)

        if configuration not in split_results:
            return False

        self.hands[player] = split_results[configuration].copy()
        self.split_count[player] += 1

        return True

    def check_winner(self):
        """Return the winner, or None if the game continues."""

        for player in (1, 2):
            opponent = 3 - player

            if self.hands[opponent] == [0, 0]:
                return player

        return None

    def switch_turn(self):
        """Switch to the other player."""

        self.current_player = 3 - self.current_player


if __name__ == "__main__":
    game = ChopsticksGame()

    print("Player 1:", game.hands[1])
    print("Player 2:", game.hands[2])

    game.attack(0, 2, 0)

    print("After Player 1 attacks:")
    print("Player 1:", game.hands[1])
    print("Player 2:", game.hands[2])
