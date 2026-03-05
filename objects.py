# objects.py - Data models for baseball player management
# Contains the Player and Lineup classes used throughout the application

class Player:
    """
    Represents a baseball player with their stats and lineup position.
    Stores personal info (name, position) and batting statistics.
    """
    
    def __init__(self, player_id=None, bat_order=0, first="", last="", pos="", ab=0, hits=0):
        # Database identifier - None for new players not yet saved
        self.id = player_id
        # Position in the batting order (1-9)
        self.order = bat_order
        # Player name fields
        self.first = first
        self.last = last
        # Field position (C, 1B, 2B, etc.)
        self.pos = pos
        # Batting statistics
        self.ab = ab      # At bats
        self.hits = hits  # Number of hits
    
    def full_name(self):
        """Returns the player's full name as a single string."""
        name = self.first + " " + self.last
        return name
    
    def avg(self):
        """
        Calculates batting average (hits divided by at bats).
        Returns 0.0 if player has no at bats to avoid division by zero.
        """
        if self.ab == 0:
            average = 0.0
        else:
            average = self.hits / self.ab
        return average


class Lineup:
    """
    Manages a list of Player objects representing the batting lineup.
    Provides methods for adding, removing, and reordering players.
    """
    
    def __init__(self):
        # Internal list to store Player objects
        self.players = []
    
    def add(self, player):
        """Adds a player to the end of the lineup."""
        self.players.append(player)
    
    def remove(self, idx):
        """Removes player at the given index if valid."""
        if idx >= 0:
            if idx < len(self.players):
                self.players.pop(idx)
    
    def move(self, old, new):
        """
        Moves a player from one position to another in the lineup.
        Both indices must be valid for the move to occur.
        """
        if old >= 0:
            if old < len(self.players):
                if new >= 0:
                    if new < len(self.players):
                        player = self.players.pop(old)
                        self.players.insert(new, player)
    
    def get(self, idx):
        """Returns the player at the given index, or None if invalid."""
        if idx >= 0:
            if idx < len(self.players):
                return self.players[idx]
        return None
    
    def count(self):
        """Returns the total number of players in the lineup."""
        num = len(self.players)
        return num
