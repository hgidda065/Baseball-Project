class Player:
    def __init__(self, player_id, bat_order, first, last, pos, ab, hits):
        self.id = player_id
        self.order = bat_order
        self.first = first
        self.last = last
        self.pos = pos
        self.ab = ab
        self.hits = hits
    
    @property
    def full_name(self):
        return f"{self.first} {self.last}"
    
    @property
    def avg(self):
        return 0.0 if self.ab == 0 else self.hits / self.ab
    
    def __repr__(self):
        return f"Player({self.id}, '{self.full_name}', {self.pos}, AVG: {self.avg:.3f})"
    
    def __str__(self):
        return f"{self.full_name} - {self.pos} (AVG: {self.avg:.3f})"
    
    def is_valid(self):
        """Validate player data"""
        return (self.hits <= self.ab and 
                self.ab >= 0 and 
                self.hits >= 0 and
                len(self.first.strip()) > 0 and
                len(self.last.strip()) > 0)


class Lineup:
    def __init__(self):
        self.players = []
    
    def add(self, player):
        self.players.append(player)
    
    def remove(self, index):
        if 0 <= index < len(self.players):
            self.players.pop(index)
    
    def move(self, old_index, new_index):
        if 0 <= old_index < len(self.players) and 0 <= new_index < len(self.players):
            player = self.players.pop(old_index)
            self.players.insert(new_index, player)
    
    def get(self, index):
        if 0 <= index < len(self.players):
            return self.players[index]
        return None
    
    def get_by_id(self, player_id):
        """Get player by ID"""
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def find_by_name(self, name_search):
        """Find players by partial name match"""
        search_lower = name_search.lower()
        return [p for p in self.players if search_lower in p.full_name.lower()]
    
    def sort_by_order(self):
        """Sort players by batting order"""
        self.players.sort(key=lambda p: p.order)
    
    def sort_by_avg(self, reverse=True):
        """Sort players by batting average"""
        self.players.sort(key=lambda p: p.avg, reverse=reverse)
    
    def clear(self):
        """Remove all players from lineup"""
        self.players.clear()
    
    def get_team_stats(self):
        """Calculate team batting statistics"""
        if not self.players:
            return {"total_ab": 0, "total_hits": 0, "team_avg": 0.0, "player_count": 0}
        
        total_ab = sum(p.ab for p in self.players)
        total_hits = sum(p.hits for p in self.players)
        team_avg = total_hits / total_ab if total_ab > 0 else 0.0
        
        return {
            "total_ab": total_ab,
            "total_hits": total_hits,
            "team_avg": team_avg,
            "player_count": len(self.players)
        }
    
    def __len__(self):
        return len(self.players)
    
    def __iter__(self):
        return iter(self.players)
    
    def __repr__(self):
        return f"Lineup({len(self.players)} players)"
    
    def __str__(self):
        if not self.players:
            return "Empty lineup"
        return f"Lineup with {len(self.players)} players"
