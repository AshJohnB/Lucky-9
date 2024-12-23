import random
import os
import json

# node and linkedlist for action history storage (playing as "{player_name}")
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display(self):
        current = self.head
        actions = []
        while current:
            actions.append(current.data)
            current = current.next
        return actions

# leaderboard system with detailed stats (playing as "{player_name}")
class Leaderboard:
    def __init__(self):
        self.file_path = "leaderboard.json"
        self.data = self.load_leaderboard()

    def load_leaderboard(self):
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            return {}

    def save_leaderboard(self):
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.data, file, indent=4)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")

    def add_game_result(self, name, result):
        if name not in self.data:
            self.data[name] = {"wins": 0, "losses": 0, "ties": 0, "total_games": 0}
        if result == "win":
            self.data[name]["wins"] += 1
        elif result == "loss":
            self.data[name]["losses"] += 1
        elif result == "tie":
            self.data[name]["ties"] += 1
        self.data[name]["total_games"] += 1
        self.save_leaderboard()

    def display(self):
        print("============================================")
        print("               LEADERBOARD")
        print("============================================")
        if not self.data:
            print("No scores yet")
        else:
            print(f"{'Name':<15} {'Wins':<5} {'Losses':<7} {'Ties':<5} {'Total Games':<12}")
            print("---------------------------------------------------------------")
            for name, stats in sorted(self.data.items(), key=lambda x: (-x[1]["wins"], x[0])):
                print(f"{name:<15} {stats['wins']:<5} {stats['losses']:<7} {stats['ties']:<5} {stats['total_games']:<12}")
        print("============================================")


# Simple custom HashMap implementation
class MyHashMap:
    def __init__(self, size=10):
        self.size = size
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def set(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return None

    def remove(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                return True
        return False

    def keys(self):
        all_keys = []
        for bucket in self.buckets:
            for pair in bucket:
                all_keys.append(pair[0])
        return all_keys

    def items(self):
        all_items = []
        for bucket in self.buckets:
            for pair in bucket:
                all_items.append((pair[0], pair[1]))
        return all_items


# Achievements system (playing as "{player_name}")
class Achievements:
    def __init__(self):
        self.file_path = "achievements.json"
        self.data_map = MyHashMap()
        self.load_achievements()

    def load_achievements(self):
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except Exception as e:
            print(f"Error loading achievements: {e}")
            data = {}

        for player_name, achievements_dict in data.items():
            self.data_map.set(player_name, achievements_dict)

    def save_achievements(self):
        data = {}
        for player_name, achievements_dict in self.data_map.items():
            data[player_name] = achievements_dict
        try:
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving achievements: {e}")

    def add_achievement(self, player_name, title, description):
        achievements_dict = self.data_map.get(player_name)
        if achievements_dict is None:
            achievements_dict = {}
        if title not in achievements_dict:
            achievements_dict[title] = description
            self.data_map.set(player_name, achievements_dict)
            self.save_achievements()

    def display_player_achievements(self, player_name):
        achievements_dict = self.data_map.get(player_name)
        if not achievements_dict:
            print("No achievements unlocked yet.")
            return
        for title, description in achievements_dict.items():
            print(f"{title}: {description}")


# NEW CLASS: Balance Manager
class BalanceManager:
    """
    Tracks each player's money using a JSON file and a MyHashMap.
    Each player's name is the key; the value is a dict with:
      { "initial_balance": int, "current_balance": int }
    """
    def __init__(self):
        self.file_path = "balances.json"
        self.data_map = MyHashMap()
        self.load_balances()

    def load_balances(self):
        """
        Load balances from the JSON file. If file is missing or corrupted,
        gracefully handle by printing an error and continuing with empty data.
        """
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
            # Ensure data is in expected format; if not, skip/correct it
            if not isinstance(data, dict):
                print("Balances file is corrupted or not in expected format. Starting fresh.")
                return
            for player_name, balances in data.items():
                # Validate that balances has required keys
                if (
                    isinstance(balances, dict)
                    and "initial_balance" in balances
                    and "current_balance" in balances
                ):
                    self.data_map.set(player_name, balances)
                else:
                    print(f"Skipping invalid balance entry for player {player_name}")
        except Exception as e:
            print(f"Error loading balances: {e}")

    def save_balances(self):
        """
        Save all balances from self.data_map to the JSON file.
        """
        data = {}
        for player_name, balances in self.data_map.items():
            data[player_name] = balances
        try:
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving balances: {e}")

    def create_or_get_balance(self, player_name):
        """
        If a player doesn't yet have a balance, create a default one.
        Otherwise, return the existing balance.
        """
        existing = self.data_map.get(player_name)
        if not existing:
            # Default new balance
            existing = {"initial_balance": 100, "current_balance": 100}
            self.data_map.set(player_name, existing)
            self.save_balances()
        return existing

    def view_balance(self, player_name):
        """
        Print out the initial and current balance for the given player.
        """
        balance_data = self.create_or_get_balance(player_name)
        print("============================================")
        print(f"Balance info for {player_name}:")
        print(f"  Initial Balance: {balance_data['initial_balance']}")
        print(f"  Current Balance: {balance_data['current_balance']}")
        print("============================================")

    def handle_win(self, player_name):
        """
        Add winnings to the player's current balance.
        """
        balance_data = self.create_or_get_balance(player_name)
        balance_data["current_balance"] += 20  # Example win amount
        self.data_map.set(player_name, balance_data)
        self.save_balances()

    def handle_loss(self, player_name):
        """
        Deduct money from the player's current balance. If the balance
        goes 0 or below, replenish a fraction of the initial balance.
        """
        balance_data = self.create_or_get_balance(player_name)
        balance_data["current_balance"] -= 10  # Example loss deduction
        if balance_data["current_balance"] <= 0:
            # Replenish fraction of the initial balance
            fraction = 0.5
            balance_data["current_balance"] = int(balance_data["initial_balance"] * fraction)
        self.data_map.set(player_name, balance_data)
        self.save_balances()


# helper functions for game logic (playing as "{player_name}")
def initialize_card_count():
    return {value: 4 for value in range(1, 11)}

def calculate_hand_total(hand):
    total = sum(card for card in hand) % 10
    return total

def calculate_probabilities(current_total, remaining_cards):
    lucky_9_count = 0
    total_possible = len(remaining_cards)
    for card in remaining_cards:
        new_total = (current_total + card) % 10
        if new_total == 9:
            lucky_9_count += 1
    if total_possible == 0:
        return 0.0
    probability_lucky_9 = (lucky_9_count / total_possible) * 100
    return probability_lucky_9

def get_valid_input(prompt, valid_choices):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_choices:
            return user_input
        print(f"Invalid input. Please enter one of {valid_choices}.")

# main game logic (playing as "{player_name}")
def play_lucky9(cards, card_count, leaderboard, player_name, achievements, balance_manager):
    player_hand = []
    banker_hand = []
    action_history = LinkedList()  # action history

    # simple fix when the deck runs out:
    if len(cards) < 6:
        print("Not enough cards to continue the game. Re-initializing deck.")
        cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 4
        random.shuffle(cards)
        card_count = initialize_card_count()

    # initial card dealing
    for _ in range(2):
        player_card = cards.pop()
        banker_card = cards.pop()
        player_hand.append(player_card)
        banker_hand.append(banker_card)
        card_count[player_card] -= 1
        card_count[banker_card] -= 1

    player_total = calculate_hand_total(player_hand)
    banker_total = calculate_hand_total(banker_hand)

    action_history.append(f"Player's initial hand: {player_hand} (total: {player_total})")
    action_history.append(f"Banker's initial hand: {banker_hand} (total: {banker_total})")

    print("============================================")
    print(f"Player's hand: {player_hand} | Total: {player_total}")
    print(f"Banker's hand: {banker_hand} | Total: {banker_total}")
    print("============================================")

    # player's turn
    if len(player_hand) < 3:
        while True:
            remaining_cards = [card for card, count in card_count.items() for _ in range(count)]
            probability_lucky_9 = calculate_probabilities(player_total, remaining_cards)
            print(f"Probability of hitting a Lucky 9: {probability_lucky_9:.2f}%")
            action = get_valid_input("Do you want to hit, stand, or view remaining cards? (hit/stand/view): ", ["hit", "stand", "view"])

            if action == 'hit':
                if len(cards) == 0:
                    print("No more cards left in the deck.")
                    action_history.append("Hit attempted, but deck empty.")
                    break
                player_card = cards.pop()
                player_hand.append(player_card)
                card_count[player_card] -= 1
                player_total = calculate_hand_total(player_hand)
                action_history.append(f"Player hits and draws: {player_card} | New total: {player_total}")
                print(f"You drew a card with value: {player_card}")
                print(f"Your cards: {player_hand} | Total: {player_total}")
                # If player hits Lucky 9, record an achievement
                if player_total == 9:
                    action_history.append("Player hits Lucky 9 and wins!")
                    achievements.add_achievement(player_name, "Lucky Nine Master", "You achieved a perfect 9!")
                break
            elif action == 'stand':
                action_history.append(f"Player stands with total: {player_total}")
                print("You chose to stand.")
                break
            elif action == 'view':
                print("Remaining cards in the deck:")
                print(card_count)

    # banker's turn
    if len(banker_hand) < 3 and (banker_total < 3 or (banker_total < 6 and player_total > banker_total)):
        banker_card = cards.pop()
        banker_hand.append(banker_card)
        card_count[banker_card] -= 1
        banker_total = calculate_hand_total(banker_hand)
        action_history.append(f"Banker draws: {banker_card} | New total: {banker_total}")

    print("============================================")
    print(f"Final Player's hand: {player_hand} | Total: {player_total}")
    print(f"Final Banker's hand: {banker_hand} | Total: {banker_total}")
    print("============================================")

    # determine winner
    if player_total > banker_total:
        print("Player wins!")
        action_history.append("Player wins!")
        leaderboard.add_game_result(player_name, "win")
        # Update balance for a win
        balance_manager.handle_win(player_name)
    elif player_total < banker_total:
        print("Banker wins!")
        action_history.append("Banker wins!")
        leaderboard.add_game_result(player_name, "loss")
        # Update balance for a loss
        balance_manager.handle_loss(player_name)
    else:
        print("It's a tie!")
        action_history.append("It's a tie!")
        leaderboard.add_game_result(player_name, "tie")
        # In a tie, do nothing to the balance (or implement your own logic if desired)

    return action_history, cards, card_count


# main entry point of the program (playing as "{player_name}")
def main():
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 4
    random.shuffle(cards)
    card_count = initialize_card_count()
    leaderboard = Leaderboard()
    achievements = Achievements()

    # Instantiate our new BalanceManager
    balance_manager = BalanceManager()

    print("============================================")
    print("         WELCOME TO LUCKY 9 GAME")
    print("============================================")
    player_name = input("Enter your name: ").strip()

    action = ""
    while True:
        print("\n============================================")
        print(f"                MAIN MENU (Playing as \"{player_name}\")")
        print("============================================")
        print("1. Play Game")
        print("2. View Leaderboard")
        print("3. Change Player Name")
        print("4. Exit")
        print("5. View Achievements")
        print("6. View Balance")  # NEW MENU OPTION
        print("============================================")
        action = get_valid_input("Choose an option: ", ["1", "2", "3", "4", "5", "6"])

        if action == "1":
            # start a new game
            action_history, cards, card_count = play_lucky9(
                cards, card_count, leaderboard, player_name, achievements, balance_manager
            )
            show_history = get_valid_input("Do you want to view the action history? (yes/no): ", ["yes", "no"])
            if show_history == 'yes':
                print("============================================")
                print(f"          ACTION HISTORY (Playing as \"{player_name}\")")
                print("============================================")
                for hist_action in action_history.display():
                    print(hist_action)

        elif action == "2":
            # display the leaderboard
            print("\n============================================")
            print(f"          CURRENT LEADERBOARD (Playing as \"{player_name}\")")
            print("============================================")
            leaderboard.display()

        elif action == "3":
            # change the player name
            player_name = input("Enter a new player name: ").strip()

        elif action == "4":
            # exit the game
            print("============================================")
            print("    THANKS FOR PLAYING! GOODBYE!")
            print("============================================")
            break

        elif action == "5":
            # View Achievements
            print("\n============================================")
            print(f"        ACHIEVEMENTS (Playing as \"{player_name}\")")
            print("============================================")
            achievements.display_player_achievements(player_name)
            print("============================================")

        elif action == "6":
            # NEW: View Balance
            balance_manager.view_balance(player_name)


if __name__ == "__main__":
    main()
