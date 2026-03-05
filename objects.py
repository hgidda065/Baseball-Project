class Player:
    def __init__(self, player_id=None, bat_order=0, first="", last="", pos="", ab=0, hits=0):
        self.id = player_id
        self.order = bat_order
        self.first = first
        self.last = last
        self.pos = pos
        self.ab = ab
        self.hits = hits
    
    def full_name(self):
        name = self.first + " " + self.last
        return name
    
    def avg(self):
        if self.ab == 0:
            average = 0.0
        else:
            average = self.hits / self.ab
        return average


class Lineup:
    def __init__(self):
        self.players = []
    
    def add(self, player):
        self.players.append(player)
    
    def remove(self, idx):
        if idx >= 0:
            if idx < len(self.players):
                self.players.pop(idx)
    
    def move(self, old, new):
        if old >= 0:
            if old < len(self.players):
                if new >= 0:
                    if new < len(self.players):
                        player = self.players.pop(old)
                        self.players.insert(new, player)
    
    def get(self, idx):
        if idx >= 0:
            if idx < len(self.players):
                return self.players[idx]
        return None
    
    def count(self):
        num = len(self.players)
        return num
