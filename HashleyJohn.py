import random
import os
import json

# node and linkedlist for action history storage (playing as "{player_name}")
class Node:
    def __init__(self, data):
        # store node data
        self.data = data
        # pointer to the next node
        self.next = None

class LinkedList:
    def __init__(self):
        # the head of the linked list
        self.head = None

    def append(self, data):
        # create a new node with the given data
        new_node = Node(data)
        # if list is empty, set head to new node
        if not self.head:
            self.head = new_node
        else:
            # otherwise, traverse to the end of the list
            current = self.head
            while current.next:
                current = current.next
            # link the last node to the new node
            current.next = new_node

    def display(self):
        # display all actions in this linked list as a list
        current = self.head
        actions = []
        # traverse through the linked list
        while current:
            actions.append(current.data)
            current = current.next
        return actions

# leaderboard system with detailed stats (playing as "{player_name}")
class Leaderboard:
    def __init__(self):
        # path for storing leaderboard data
        self.file_path = "leaderboard.json"
        # load existing data from file
        self.data = self.load_leaderboard()

    def load_leaderboard(self):
        # load leaderboard data from json file if it exists
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            return {}

    def save_leaderboard(self):
        # save current leaderboard data to the json file
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.data, file, indent=4)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")

    def add_game_result(self, name, result):
        # if the player doesn't exist, initialize their record
        if name not in self.data:
            self.data[name] = {"wins": 0, "losses": 0, "ties": 0, "total_games": 0}
        # update records based on the result
        if result == "win":
            self.data[name]["wins"] += 1
        elif result == "loss":
            self.data[name]["losses"] += 1
        elif result == "tie":
            self.data[name]["ties"] += 1
        # increment total games
        self.data[name]["total_games"] += 1
        # save the updated leaderboard
        self.save_leaderboard()

    def display(self):
        # display the leaderboard in a table-like format
        print("============================================")
        print("               LEADERBOARD")
        print("============================================")
        if not self.data:
            print("No scores yet")
        else:
            print(f"{'Name':<15} {'Wins':<5} {'Losses':<7} {'Ties':<5} {'Total Games':<12}")
            print("---------------------------------------------------------------")
            # sort players by highest wins first, then by name
            for name, stats in sorted(self.data.items(), key=lambda x: (-x[1]["wins"], x[0])):
                print(f"{name:<15} {stats['wins']:<5} {stats['losses']:<7} {stats['ties']:<5} {stats['total_games']:<12}")
        print("============================================")


# simple custom hashmap implementation
class MyHashMap:
    def __init__(self, size=10):
        # create a list of buckets, each bucket is a list of [key, value] pairs
        self.size = size
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        # compute hash index by built-in hash function modded by size
        return hash(key) % self.size

    def set(self, key, value):
        # set or update the value for the given key
        index = self._hash(key)
        bucket = self.buckets[index]
        # if key already exists, update it; otherwise, append a new pair
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key):
        # retrieve the value for the given key, or none if not found
        index = self._hash(key)
        bucket = self.buckets[index]
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return None

    def remove(self, key):
        # remove the key-value pair if it exists
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                return True
        return False

    def keys(self):
        # return a list of all keys in the hashmap
        all_keys = []
        for bucket in self.buckets:
            for pair in bucket:
                all_keys.append(pair[0])
        return all_keys

    def items(self):
        # return a list of all (key, value) pairs in the hashmap
        all_items = []
        for bucket in self.buckets:
            for pair in bucket:
                all_items.append((pair[0], pair[1]))
        return all_items


# achievements system (playing as "{player_name}")
class Achievements:
    def __init__(self):
        # file path for achievements data
        self.file_path = "achievements.json"
        # store achievements data in a hashmap
        self.data_map = MyHashMap()
        self.load_achievements()

    def load_achievements(self):
        # load achievements from file if it exists
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except Exception as e:
            print(f"Error loading achievements: {e}")
            data = {}

        # insert achievements into the hashmap
        for player_name, achievements_dict in data.items():
            self.data_map.set(player_name, achievements_dict)

    def save_achievements(self):
        # extract achievements from hashmap and save to json
        data = {}
        for player_name, achievements_dict in self.data_map.items():
            data[player_name] = achievements_dict
        try:
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving achievements: {e}")

    def add_achievement(self, player_name, title, description):
        # add a new achievement under the given player's record
        achievements_dict = self.data_map.get(player_name)
        if achievements_dict is None:
            achievements_dict = {}
        # if the title doesn't exist, create it
        if title not in achievements_dict:
            achievements_dict[title] = description
            self.data_map.set(player_name, achievements_dict)
            self.save_achievements()

    def display_player_achievements(self, player_name):
        # display all achievements for a given player
        achievements_dict = self.data_map.get(player_name)
        if not achievements_dict:
            print("No achievements unlocked yet.")
            return
        for title, description in achievements_dict.items():
            print(f"{title}: {description}")


# new class: balance manager
class BalanceManager:
    """
    tracks each player's money using a json file and a myhashmap.
    each player's name is the key; the value is a dict with:
      {
        "initial_balance": int,
        "current_balance": int
      }
    """
    def __init__(self):
        # path to balances json file
        self.file_path = "balances.json"
        # myhashmap to store player balance data
        self.data_map = MyHashMap()
        self.load_balances()

    def load_balances(self):
        """
        load balances from the json file. if file is missing or corrupted,
        gracefully handle by printing an error and continuing with empty data.
        """
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
            # check if data is a valid dict
            if not isinstance(data, dict):
                print("Balances file is corrupted or not in expected format. Starting fresh.")
                return
            # load each player's balances into the hashmap
            for player_name, balances in data.items():
                if (isinstance(balances, dict)
                    and "initial_balance" in balances
                    and "current_balance" in balances):
                    self.data_map.set(player_name, balances)
                else:
                    print(f"Skipping invalid balance entry for player {player_name}")
        except Exception as e:
            print(f"Error loading balances: {e}")

    def save_balances(self):
        """
        save all balances from self.data_map to the json file.
        """
        data = {}
        # build a dictionary to save from the myhashmap data
        for player_name, balances in self.data_map.items():
            data[player_name] = balances
        try:
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving balances: {e}")

    def create_or_get_balance(self, player_name):
        """
        if a player doesn't yet have a balance, create a default one.
        otherwise, return the existing balance.
        """
        existing = self.data_map.get(player_name)
        # if no record, create one with default values
        if not existing:
            existing = {"initial_balance": 100, "current_balance": 100}
            self.data_map.set(player_name, existing)
            self.save_balances()
        return existing

    def view_balance(self, player_name):
        """
        print out the initial, current balance, and also the profit.
        """
        balance_data = self.create_or_get_balance(player_name)
        profit = balance_data['current_balance'] - balance_data['initial_balance']
        print("============================================")
        print(f"Balance info for {player_name}:")
        print(f"  Initial Balance: {balance_data['initial_balance']}")
        print(f"  Current Balance: {balance_data['current_balance']}")
        print(f"  Profit: {profit}")
        print("============================================")

    def handle_win(self, player_name, bet=20):
        """
        add 'bet' to the player's current balance.
        """
        balance_data = self.create_or_get_balance(player_name)
        balance_data["current_balance"] += bet
        self.data_map.set(player_name, balance_data)
        self.save_balances()

    def handle_loss(self, player_name, bet=10):
        """
        deduct 'bet' from the player's current balance. if balance <= 0,
        replenish half of the initial balance.
        """
        balance_data = self.create_or_get_balance(player_name)
        balance_data["current_balance"] -= bet
        if balance_data["current_balance"] <= 0:
            fraction = 0.5
            balance_data["current_balance"] = int(balance_data["initial_balance"] * fraction)
        self.data_map.set(player_name, balance_data)
        self.save_balances()


# helper functions for game logic (playing as "{player_name}")
def initialize_card_count():
    # return a dictionary for card values 1-10, each with 4 occurrences
    return {value: 4 for value in range(1, 11)}

def calculate_hand_total(hand):
    # sum the card values and mod by 10 to get the lucky 9 total
    return sum(card for card in hand) % 10

def calculate_probabilities(current_total, remaining_cards):
    # calculate the probability of hitting lucky 9 if drawing another card
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
    # repeatedly prompt the user until valid input is entered
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_choices:
            return user_input
        print(f"Invalid input. Please enter one of {valid_choices}.")


def get_valid_bet(balance_manager, player_name):
    """
    prompt the player to enter a bet between 1 and their current balance.
    includes robust error handling for non-integer inputs and out-of-range bets.
    """
    while True:
        balance_data = balance_manager.create_or_get_balance(player_name)
        current_balance = balance_data["current_balance"]
        # if no funds, return 0 bet
        if current_balance <= 0:
            print(f"{player_name}, your balance is 0. Cannot place a bet.")
            return 0
        bet_input = input(f"Enter your bet amount (1 - {current_balance}): ").strip()
        # check if input is a digit
        if not bet_input.isdigit():
            print("Invalid input. Please enter a valid number.")
            continue
        bet = int(bet_input)
        # check if bet is within allowable range
        if bet < 1 or bet > current_balance:
            print(f"Invalid bet amount. Must be between 1 and {current_balance}.")
            continue
        return bet


# main game logic (playing as "{player_name}")
def play_lucky9(cards, card_count, leaderboard, player_name, achievements, balance_manager):
    # first, get a valid bet from the player
    bet_amount = get_valid_bet(balance_manager, player_name)
    # if bet is 0, skip the round
    if bet_amount == 0:
        print(f"{player_name} has insufficient funds or bet was invalid. Round skipped.")
        return LinkedList(), cards, card_count

    player_hand = []
    banker_hand = []
    action_history = LinkedList()

    # if deck is too small, reinitialize
    if len(cards) < 6:
        print("Not enough cards to continue the game. Re-initializing deck.")
        cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 4
        random.shuffle(cards)
        card_count = initialize_card_count()

    # deal initial cards to player and banker
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

    # player's decision (hit, stand, or view)
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
                # if player hits a lucky 9, record the achievement
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

    # banker logic for drawing a third card
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

    # decide outcome: player win, banker win, or tie
    if player_total > banker_total:
        print("Player wins!")
        action_history.append("Player wins!")
        leaderboard.add_game_result(player_name, "win")
        # update balance for a win using the bet
        balance_manager.handle_win(player_name, bet=bet_amount)
    elif player_total < banker_total:
        print("Banker wins!")
        action_history.append("Banker wins!")
        leaderboard.add_game_result(player_name, "loss")
        # update balance for a loss using the bet
        balance_manager.handle_loss(player_name, bet=bet_amount)
    else:
        print("It's a tie!")
        action_history.append("It's a tie!")
        leaderboard.add_game_result(player_name, "tie")
        # ties do not alter balance

    return action_history, cards, card_count


# main entry point of the program (playing as "{player_name}")
def main():
    # initialize the deck and randomize it
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 4
    random.shuffle(cards)
    # keep track of card counts for each card value
    card_count = initialize_card_count()
    # create leaderboard instance
    leaderboard = Leaderboard()
    # create achievements instance
    achievements = Achievements()
    # create balance manager instance
    balance_manager = BalanceManager()

    # prompt for the player's name
    player_name = input("Enter your name: ").strip()

    while True:
        # get the current balance for the header display
        balance_info = balance_manager.create_or_get_balance(player_name)
        current_balance = balance_info["current_balance"]

        # bigger header showcasing player name and current balance
        print("\n==============================================================")
        print(f"      WELCOME TO LUCKY 9 GAME (Playing as \"{player_name}\")")
        print(f"                   Current Balance: {current_balance}")
        print("==============================================================")

        # display the main menu of options
        print("1. Play Game")
        print("2. View Leaderboard")
        print("3. Change Player Name")
        print("4. Exit")
        print("5. View Achievements")
        print("6. View Balance")
        print("==============================================================")

        action = get_valid_input("Choose an option: ", ["1", "2", "3", "4", "5", "6"])

        if action == "1":
            # play a new round of lucky 9
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
            # show the leaderboard
            print("\n============================================")
            print(f"          CURRENT LEADERBOARD (Playing as \"{player_name}\")")
            print("============================================")
            leaderboard.display()

        elif action == "3":
            # let the user change their player name
            player_name = input("Enter a new player name: ").strip()

        elif action == "4":
            # exit the program
            print("============================================")
            print("    THANKS FOR PLAYING! GOODBYE!")
            print("============================================")
            break

        elif action == "5":
            # display achievements for current player
            print("\n============================================")
            print(f"        ACHIEVEMENTS (Playing as \"{player_name}\")")
            print("============================================")
            achievements.display_player_achievements(player_name)
            print("============================================")

        elif action == "6":
            # view balance info (includes profits)
            balance_manager.view_balance(player_name)


if __name__ == "__main__":
    main()
