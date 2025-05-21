# Avalon CLI Game

This is a command-line version of the social deduction game **Avalon**, written in Python. Players take on hidden roles as members of the Good or Evil factions and work through rounds of voting, deception, and deduction.

---

## 🎮 How to Play

### Overview

- A leader proposes a team to go on a quest.
- All players vote to approve or reject the proposed team.
- If approved, team members secretly vote to either **succeed** or **fail** the quest.
- Good wins if **3 quests succeed**.
- Evil wins if **3 quests fail**, or if **Assassin correctly identifies Merlin** after 3 successful quests.

---

## 🧙‍♂️ Roles

Each player receives a secret role:

### Good
- **Merlin**: Knows evil players (except Mordred)
- **Percival**: Knows two players, one of whom is Merlin, one is Morgana
- **Loyal Servant**: No special powers

### Evil
- **Assassin**: Attempts to identify Merlin at the end
- **Morgana**: Appears as Merlin to Percival
- **Mordred**: Hidden from Merlin
- **Oberon**: Does not know other evil players, and they don’t know him
- **Minion of Mordred**: A regular evil agent

---

## 🛠 How to Run

1. Make sure you have Python 3 installed.
2. Clone this repository or download the source files.
3. Run the game:

```bash
python game.py

