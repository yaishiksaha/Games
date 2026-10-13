
import tkinter as tk
from game import ChopsticksGame


class ChopsticksGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chopsticks")
        self.root.geometry("600x520")
        self.root.resizable(False, False)

        self.game = ChopsticksGame()

        # The GUI uses these variables to track the selected action
        # and the attacking hand.
        self.selected_action = None
        self.attacking_hand = None
        self.game_over = False

        # Title
        tk.Label(
            root,
            text="CHOPSTICKS",
            font=("Arial", 24, "bold")
        ).pack(pady=12)

        self.turn_label = tk.Label(
            root,
            text="Player 1's Turn",
            font=("Arial", 16, "bold")
        )
        self.turn_label.pack(pady=5)

        # Player hands
        self.hands_frame = tk.Frame(root)
        self.hands_frame.pack(pady=12)

        self.hand_buttons = {}

        for player in (1, 2):
            player_frame = tk.LabelFrame(
                self.hands_frame,
                text=f"Player {player}",
                font=("Arial", 12, "bold"),
                padx=12,
                pady=12
            )
            player_frame.grid(
                row=0,
                column=player - 1,
                padx=12
            )

            for hand_index, hand_name in enumerate(("Left", "Right")):
                button = tk.Button(
                    player_frame,
                    text=f"{hand_name}\n1",
                    font=("Arial", 14),
                    width=9,
                    height=3,
                    command=lambda p=player, h=hand_index:
                        self.select_hand(p, h)
                )
                button.grid(
                    row=0,
                    column=hand_index,
                    padx=4
                )

                self.hand_buttons[(player, hand_index)] = button

        # Action buttons
        actions_frame = tk.Frame(root)
        actions_frame.pack(pady=12)

        tk.Button(
            actions_frame,
            text="Attack",
            width=12,
            command=self.choose_attack
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            actions_frame,
            text="Increment",
            width=12,
            command=self.choose_increment
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            actions_frame,
            text="Split",
            width=12,
            command=self.choose_split
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(
            actions_frame,
            text="Cancel Action",
            width=12,
            command=self.cancel_action
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            actions_frame,
            text="Restart",
            width=12,
            command=self.restart_game
        ).grid(row=1, column=1, padx=5, pady=5)

        # Message area
        self.message_label = tk.Label(
            root,
            text="Choose an action.",
            font=("Arial", 11),
            wraplength=540
        )
        self.message_label.pack(pady=10)

        self.update_display()

    def choose_attack(self):
        if self.game_over:
            return

        self.selected_action = "attack"
        self.attacking_hand = None

        self.message_label.config(
            text=(
                "Select your attacking hand first, "
                "then select the target hand."
            )
        )

    def choose_increment(self):
        if self.game_over:
            return

        self.selected_action = "increment"
        self.attacking_hand = None

        self.message_label.config(
            text="Select one of your active hands to increment."
        )

    def choose_split(self):
        if self.game_over:
            return

        self.selected_action = "split"
        self.attacking_hand = None

        player = self.game.current_player

        if self.game.split_count[player] >= 3:
            self.message_label.config(
                text="You have already used all three splits."
            )
            return

        if not self.game.split():
            self.message_label.config(
                text="You cannot split this hand configuration."
            )
            return

        self.finish_turn(
            f"Player {player} split their hands."
        )

    def select_hand(self, player, hand_index):
        if self.game_over:
            return

        current_player = self.game.current_player

        # Increment: select one of your own hands.
        if self.selected_action == "increment":
            if player != current_player:
                self.message_label.config(
                    text="You can only increment your own hand."
                )
                return

            if not self.game.increment(hand_index):
                self.message_label.config(
                    text="That hand is eliminated and cannot be incremented."
                )
                return

            hand_name = ("left", "right")[hand_index]

            self.finish_turn(
                f"Player {player} incremented their {hand_name} hand."
            )
            return

        # Attack: select the attacking hand, then the target.
        if self.selected_action == "attack":

            if self.attacking_hand is None:
                if player != current_player:
                    self.message_label.config(
                        text="Select one of your own hands first."
                    )
                    return

                if self.game.hands[player][hand_index] == 0:
                    self.message_label.config(
                        text="An eliminated hand cannot attack."
                    )
                    return

                self.attacking_hand = hand_index

                hand_name = ("left", "right")[hand_index]

                self.message_label.config(
                    text=(
                        f"Attacking hand: {hand_name}. "
                        "Now select the target hand."
                    )
                )
                return

            # The player has already selected an attacking hand.
            attacker_hand = self.attacking_hand

            if player == current_player and hand_index == attacker_hand:
                self.message_label.config(
                    text="Choose a different hand as the target."
                )
                return

            if self.game.hands[player][hand_index] == 0:
                self.message_label.config(
                    text="You cannot attack an eliminated hand."
                )
                return

            if not self.game.attack(
                attacker_hand,
                player,
                hand_index
            ):
                self.message_label.config(
                    text="Invalid attack. Please select another target."
                )
                return

            attacker_name = ("left", "right")[attacker_hand]
            target_name = ("left", "right")[hand_index]

            self.finish_turn(
                f"Player {current_player} used their {attacker_name} "
                f"hand to attack Player {player}'s {target_name} hand."
            )

    def finish_turn(self, message):
        winner = self.game.check_winner()

        self.selected_action = None
        self.attacking_hand = None

        if winner is not None:
            self.game_over = True
            self.update_display()

            self.message_label.config(
                text=f"{message}\nPlayer {winner} wins!"
            )
            return

        self.game.switch_turn()
        self.update_display()

        self.message_label.config(
            text=f"{message}\nPlayer {self.game.current_player}'s turn."
        )

    def cancel_action(self):
        if self.game_over:
            return

        self.selected_action = None
        self.attacking_hand = None

        self.message_label.config(
            text="Action cancelled. Choose another action."
        )

        self.update_display()

    def restart_game(self):
        self.game = ChopsticksGame()
        self.selected_action = None
        self.attacking_hand = None
        self.game_over = False

        self.update_display()

        self.message_label.config(
            text="New game started. Player 1 goes first."
        )

    def update_display(self):
        for player in (1, 2):
            for hand_index, hand_name in enumerate(("Left", "Right")):
                value = self.game.hands[player][hand_index]
                button = self.hand_buttons[(player, hand_index)]

                button.config(
                    text=f"{hand_name}\n{value}",
                    state="normal" if value != 0 and not self.game_over
                    else "disabled"
                )

        self.turn_label.config(
            text=(
                "GAME OVER"
                if self.game_over
                else f"Player {self.game.current_player}'s Turn"
            )
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ChopsticksGUI(root)
    root.mainloop()
