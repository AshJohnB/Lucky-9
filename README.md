# Lucky-9
Final Project for Data Structures (Submitted to Prof. Louis Velasco)

# Lucky 9 Game Program

## Overview
The **Lucky 9 Game** is a card game that combines strategy, probability, and fun! This program allows players to:
- Compete against a virtual banker.
- Track their wins, losses, and ties on a leaderboard.
- Unlock achievements for their gameplay.
- Manage their virtual balance through betting.

## Features
1. **Leaderboards**: See rankings based on wins, losses, and total games.
2. **Achievements**: Unlock special achievements as you play.
3. **Balance Management**: Track and manage in-game virtual currency with betting functionality.
4. **Action History**: View a detailed history of your moves during each game.

## How to Use

### Starting the Game
1. Run the program:
   ```bash
   python HashleyJohn.py
   ```
2. Enter your name to start the session.

### Main Menu Options
1. **Play Game**: Start a new round of Lucky 9. Bet an amount and try to beat the banker.
2. **View Leaderboard**: Check the standings of all players based on their wins and losses.
3. **Change Player Name**: Switch to a new player profile.
4. **Exit**: Quit the game.
5. **View Achievements**: See the list of achievements you've unlocked.
6. **View Balance**: Check your current and initial balance, as well as your profit/loss.

### Gameplay
- The objective is to achieve a hand total as close to 9 as possible.
- You'll start with two cards and decide whether to "hit" (draw another card) or "stand."
- The banker will also play strategically based on its cards.
- If your total is closer to 9 than the banker’s, you win!

### Betting
- Each round requires a bet.
- If you win, the bet amount is added to your balance.
- If you lose, the bet amount is deducted. If your balance drops to 0, it’s replenished to half of your initial balance.

### Achievements
Achievements are awarded for specific milestones, such as hitting a "Lucky 9" during gameplay.

### Leaderboard
Player statistics, including wins, losses, and ties, are saved and ranked in the leaderboard.

## Saving and Loading
- **Leaderboard** and **Achievements** are automatically saved and loaded from `leaderboard.json` and `achievements.json`, respectively.
- Player balances are managed in `balances.json`.

## Requirements
- Python 3.x
- JSON files (`leaderboard.json`, `achievements.json`, `balances.json`) are created automatically if not present.

## Notes
- Ensure the JSON files are not manually modified to avoid data corruption.
- If the deck runs out of cards, it is reshuffled automatically.

Let's all have fun and play together!

