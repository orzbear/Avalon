import sys
import player
from utils import clear_screen
import game_logic

def main():
    # Start of the game
    """Main entry point for the game."""
    print("""
=== Welcome to Avalon ===

Avalon is a game of deception and deduction.

Each round:
- A leader proposes a team to go on a quest.
- All players vote to approve or reject the team.
- If approved, the quest team secretly votes to succeed or fail the quest.
- The good team wins if 3 quests succeed.
- The evil team wins if 3 quests fail.
- If 3 quests succeed, the Assassin gets one chance to guess who Merlin is — if correct, evil wins!

Get ready...

""")


    players = []
    while True:
        num_input = input("Enter the number of players (5–10): ")
        if not num_input.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        num_players = int(num_input)
        if 5 <= num_players <= 10:
            break
        else:
            print("Invalid number of players. Please enter a number between 5 and 10.")

    
    for i in range(num_players):
        name = input(f"Enter the name of player {i + 1}: ")
        players.append(name)
    
    game = game_logic.Game(players)
    game.assign_roles()

    print("Roles have been assigned.")
    print("\nEach player can now check their own role.\n")    
    for player in game.players:
        input(f"{player.name}, press Enter to view your role (others please look away).")

        print(f"\n{player.name}, your role is: {player.role}")
        print(f"You are on the {player.party.upper()} team.\n")

        if player.role == "Merlin":
            known_evil = [p.name for p in game.players if p.party == "bad" and p.role != "Mordred"]
            print("As Merlin, you can sense the following evil players (excluding Mordred):")
            print(", ".join(known_evil) if known_evil else "None")

        elif player.role == "Percival":
            merlin = next((p.name for p in game.players if p.role == "Merlin"), None)
            morgana = next((p.name for p in game.players if p.role == "Morgana"), None)
            suspects = [name for name in [merlin, morgana] if name]
            print("As Percival, you sense these two players (one is Merlin, one is Morgana):")
            print(", ".join(suspects) if suspects else "Not enough suspects in play.")

        elif player.party == "bad":
            if player.role == "Oberon":

                print("You are Oberon and do not know your teammates.")
            else:
                teammates = [p.name for p in game.players if p.party == "bad" and p.name != player.name and p.role != "Oberon"]
                print("Your fellow evil teammates are:")
                print(", ".join(teammates) if teammates else "You are the only visible evil player.")

        input("\nPress Enter to continue...")
        clear_screen()


    print("""
=== Avalon Role Overview ===
Good Roles:
- Merlin: Knows who the bad players are but must stay hidden.
- Percival: Knows who Merlin is (or at least two suspects if Morgana is in play).
- Loyal Servant: Regular good player.

Bad Roles:
- Assassin: Tries to find and kill Merlin at the end.
- Morgana: Appears as Merlin to Percival.
- Mordred: Hidden from Merlin.
- Oberon: Does not know the other bad players.

            """)
    
    # role reveal for testing

    # for player in game.players:
    #     if player.party == "good" or player.role == "Oberon":
    #         # Good players and Oberon can see their own role
    #         print(f"{player.name} is a {player.role}. {player.party} party")
    #     else:
    #         evil = [p.name for p in game.players if p.party == "bad" ]
    #         print(f"Evil players: {', '.join(evil)}")
    #         print(f"{player.name} is a {player.role}. {player.party} party")


    # Game loop
    while True:
        print(f"Round {game.rounds + 1}")
        game.check_status()
        # Assign roles and leader
        game.assign_leader()
        # Leader selects team

        #Re-check their roles in case they forget
        while True:
            check = input("Type 'check' to see game status, or 'check role' to see your own role: ")
            if check.lower() == "check":
                game.check_status()
            elif check.lower() == "check role":
                name = input("Enter your name to check your role: ")
                game.check_roles(name)
                clear_screen()
            else:
                break

            

        selected_team = game.team_selection()
        print("Selected team:", [player.name for player in selected_team])
        
        # Voting phase
        if not game.voting_team():
            continue

        # Quest phase
        game.voting_quest(selected_team)

        game.rotate_leader()

        # Check if the game has ended
        if game.check_end():
            break
        else:
            game.rounds += 1

    # End of the game
    if game.good_win:
        print("Good team wins!")
    elif game.bad_win:
        print("Evil team wins!")
    
    print("\n=== Final Roles ===")
    for player in game.players:
        print(f"{player.name} — {player.role} ({player.party})")



if __name__ == "__main__":
    main()