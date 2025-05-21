class Player:
    def __init__(self, name):
        """
        Initialize a new player with a name and role.
        """
        self.name = name
        self.role = None
        self.party = None
        self.leader = False  # To indicate if the player is the leader
        self.vote = None  # To store the player's vote
    
    def set_role(self, role):

        """
        Set the player's role.
        """
        self.role = role


    def set_party(self, party):
        """
        Set the player's party affiliation based on the role.
        """
        self.party = party 


    def is_good(self):
        """
        Check if the player is on the good team.
        """
        return self.party == 'good'
    
    def is_bad(self):
        """
        Check if the player is on the bad team.
        """
        return self.party == 'bad'
    
    def reset_vote(self):
        """
        Reset the player's vote.
        """
        self.vote = None


    def cast_vote(self, vote):
        """
        Cast a vote (e.g., 'y' or 'n').
        """
        if vote.lower() in ['y', 'n']:
            self.vote = vote.lower()
            print(f"{self.name} cast their vote: {self.vote}")
        else:
            print("Invalid vote. Please vote 'y' or 'n'.")



    def __str__(self):
        """
        Return a string representation of the player.
        """
        return f"Player(name={self.name}, role={self.role}, vote={self.vote})"
