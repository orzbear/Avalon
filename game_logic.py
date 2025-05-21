
from player import Player
from utils import shuffle_players
from utils import clear_screen

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.good_win = False
        self.bad_win = False
        self.rounds = 0
        self.leader_index = 0
        self.quest_records = {"Approved": 0, "Failed": 0}
        self.team_failures = 0
        
        
        self.role_party_map = {
        "Merlin": "good",
        "Percival": "good",
        "Loyal Servant": "good",
        "Assassin": "bad",
        "Morgana": "bad",
        "Minion of Mordred": "bad",
        "Mordred": "bad",
        "Oberon": "bad"}

        self.role_presets = {
                5: ["Merlin", "Assassin", "Percival", "Morgana", "Loyal Servant"],
                6: ["Merlin", "Assassin", "Percival", "Morgana", "Loyal Servant", "Loyal Servant"],
                7: ["Merlin", "Assassin", "Percival", "Morgana", "Loyal Servant", "Loyal Servant", "Minion of Mordred"],
                8: ["Merlin", "Assassin", "Percival", "Morgana", "Mordred", "Loyal Servant", "Loyal Servant", "Loyal Servant"],
                9: ["Merlin", "Assassin", "Percival", "Morgana", "Mordred", "Loyal Servant", "Loyal Servant", "Loyal Servant", 
                    "Minion of Mordred"],
                10: ["Merlin", "Assassin", "Percival", "Morgana", "Mordred", "Oberon", "Loyal Servant", "Loyal Servant", 
                     "Loyal Servant", "Loyal Servant"]
            }
        
        self.quest_team_sizes = {
                5: [2, 3, 2, 3, 3],
                6: [2, 3, 4, 3, 4],
                7: [2, 3, 3, 4, 4],
                8: [3, 4, 4, 5, 5],
                9: [3, 4, 4, 5, 5],
                10:[3, 4, 4, 5, 5]
            }

        
        self.roles = self.role_presets[len(self.players)]
        self.current_leader = 0  # Index of the player choosing team

    def assign_roles(self):
        """
        Assign roles to players based on the number of players.
        """
        player_count = len(self.players)
        if player_count not in self.role_presets:
            print("Unsupported player count.")
            return

        selected_roles = self.role_presets[player_count]
        shuffled_roles = shuffle_players(selected_roles[:])

        for player, role in zip(self.players, shuffled_roles):
            player.set_role(role)
            player.set_party(self.role_party_map[role])

    
    def assign_leader(self):
        """
        Assign the leader for the current round.    
        """
        self.players[self.leader_index].leader = True
        print(f"{self.players[self.leader_index].name} is the current leader.")

    def role_check(self, name):
        for player in self.players:
            if player.name == name:
                print(f"{player.name}'s role: {player.role}")
                return
        print("Player not found.")

    def team_selection(self) -> list:
        """
        Selects a team for the quest based on the current leader's choice.
        Returns a list of selected players.
        """
        selected_team = []
        for player in self.players:
            if player.leader:
                print(f"{player.name} is the leader and will select the team.")
                break

        team_size = self.quest_team_sizes[len(self.players)][self.rounds]
        print(f"Team size for this quest: {team_size}")
        while len(selected_team) < team_size:
            player_name = input(f"Select a player for the team (remaining spots: {team_size - len(selected_team)}): ")
            for player in self.players:
                if player.name == player_name and player not in selected_team:
                    selected_team.append(player)
                    print(f"{player.name} has been added to the team.")
                    break
            else:
                print("Invalid selection. Please try again.") 
        
        return selected_team
    
    def assassin_phase(self) -> str:
        """
        The Assassin phase where the Assassin can choose to eliminate a player.
        """
        assassin = None
        target = None
        for player in self.players:
            if player.role == "Assassin":
                assassin = player
                break

        print(f"{assassin.name}, you are the Assassin. You can eliminate a player.")
        while not target and assassin:
            target_name = input("Enter the name of the player you want to eliminate: ")
            for player in self.players:
                if player.name == target_name and player != assassin:
                    target = player
                    print(f"{assassin.name} has eliminated {player.name}. He is {player.role}.")
                    return target
            else:
                print("Invalid target. No one was eliminated.")
    

    def check_end(self) -> bool:
        """
        Check if the game has been won by either team.
        """
        if self.quest_records["Approved"] == 3:
            target = self.assassin_phase()
            if target.role == "Merlin":
                self.bad_win = True
                print("Evil team wins!")
                return True
            else:
                self.good_win = True
                return True
        elif self.quest_records["Failed"] == 3:
            self.bad_win = True
            return True
    
    def voting_team(self) -> bool:
        """
        Vote on the selected team for the quest.
        """
        votes_y = 0
        votes_n = 0 
        votes =  {}   
        for player in self.players:
            vote = input(f"{player.name}, do you approve the team? (y/n): ")
            while vote.lower() not in ['y', 'n']:
                print("Invalid vote. Please vote 'y' or 'n'.")
                vote = input(f"{player.name}, do you approve the team? (y/n): ")
            if vote.lower() == 'y':
                votes_y += 1
            elif vote.lower() == 'n':
                votes_n += 1
            votes[player.name] = vote.lower()
        
        required_votes = len(self.players) // 2 + 1

        print(f"Votes: {votes}")
        print(f"Votes in favor: {votes_y}, Votes against: {votes_n}")
        
        if votes_y >= required_votes:
            print("Team approved for the quest.")
            self.leader_index = (self.leader_index + 1) % len(self.players)
            self.players[self.leader_index].leader = True
            self.players[(self.leader_index - 1) % len(self.players)].leader = False
            return True
        else:
            print("Team rejected. A new team must be selected.")

            self.leader_index = (self.leader_index + 1) % len(self.players)
            self.players[self.leader_index].leader = True
            self.players[(self.leader_index - 1) % len(self.players)].leader = False
            return False

    
    def voting_quest(self, team):
        """
        Vote on the quest.
        """
        quest_failed = False
        for player in team:
            vote = input(f"{player.name}, do you approve the quest? If you are in the good side, you must vote for y (y/n): ")
            if player.is_good():
                vote = "y"
            while vote.lower() not in ['y', 'n']:
                print("Invalid vote. Please vote 'y' or 'n'.")
                vote = input(f"{player.name}, do you approve the quest? If you are in the good side, you must vote for y (y/n): ")
            clear_screen()
            if vote.lower() == 'n':
                quest_failed = True

        if quest_failed:
            print("Quest Failed.")
            self.quest_records["Failed"] += 1
        else:
            print("Quest Approved.")
            self.quest_records["Approved"] += 1

    def rotate_leader(self):
        self.players[self.leader_index].leader = False
        self.leader_index = (self.leader_index + 1) % len(self.players)
        self.players[self.leader_index].leader = True

    def check_status(self):
        print("\n=== Game Status ===")
        print(f"Round: {self.rounds + 1}")
        print(f"Successful Quests: {self.quest_records['Approved']}")
        print(f"Failed Quests: {self.quest_records['Failed']}")
        print("====================\n")
    
    def check_roles(self, name):
        from utils import clear_screen
        import random

        player = next((p for p in self.players if p.name == name), None)
        if not player:
            print("Player not found.")
            return

        print(f"\n{player.name}'s role: {player.role}, {player.party.upper()} party")

        if player.role == "Merlin":
            known_evil = [p.name for p in self.players if p.party == "bad" and p.role != "Mordred"]
            print("You can sense the following evil players (excluding Mordred):")
            print(", ".join(known_evil))

        elif player.role == "Percival":
            merlin = next((p.name for p in self.players if p.role == "Merlin"), None)
            morgana = next((p.name for p in self.players if p.role == "Morgana"), None)
            suspects = [n for n in [merlin, morgana] if n]
            random.shuffle(suspects)
            print("You sense two players — one is Merlin, one is Morgana:")
            print(", ".join(suspects))

        elif player.party == "bad":
            if player.role == "Oberon":
                print("You are Oberon and do not know your fellow evil teammates.")
            else:
                teammates = [p.name for p in self.players if p.party == "bad" and p.name != player.name and p.role != "Oberon"]
                print("Your fellow evil teammates are:")
                print(", ".join(teammates))

        input("\nPress Enter to continue...")
        clear_screen()





